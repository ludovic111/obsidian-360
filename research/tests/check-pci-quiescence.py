#!/usr/bin/env python3
"""Run pinned PCI core functions with injected configuration access outcomes.

No hardware access. A positive generic helper result is not a Xenon DMA fence.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile


def extract(text, name):
    match = re.search(r'^(?:static )?(?:inline )?[\w *]+\b' + name + r'\([^;]*?\n\{', text, re.M)
    if not match:
        raise ValueError('Function absent: ' + name)
    return text[match.start():text.index('\n}', match.end()) + 2]


PREFIX = r'''
#include <assert.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
typedef uint8_t u8;
typedef uint16_t u16;
#define PCI_COMMAND 4
#define PCI_COMMAND_MASTER 4
#define PCI_STATUS 6
#define PCI_STATUS_CAP_LIST 16
#define PCI_HEADER_TYPE_NORMAL 0
#define PCI_HEADER_TYPE_BRIDGE 1
#define PCI_HEADER_TYPE_CARDBUS 2
#define PCI_CAPABILITY_LIST 52
#define PCI_CB_CAPABILITY_LIST 20
#define PCI_EXP_DEVSTA 10
#define PCI_EXP_DEVSTA_TRPND 32
struct pci_bus { u16 status; };
struct pci_dev { bool is_busmaster; int pcie_cap; u16 command; };
static unsigned reads, writes, sleeps, slept_ms, bus_reads, next_status;
static u16 statuses[4];
static bool write_fails;
#define pci_dbg(...) ((void)0)
static int pci_bus_read_config_word(struct pci_bus *b, unsigned fn, int pos, u16 *out) {
    assert(fn == 0 && pos == PCI_STATUS); ++bus_reads; *out=b->status; return 0;
}
static int pci_read_config_word(struct pci_dev *d, int pos, u16 *out) {
    ++reads;
    if (pos==PCI_COMMAND) *out=d->command;
    else { assert(pos==d->pcie_cap+PCI_EXP_DEVSTA); assert(next_status<4); *out=statuses[next_status++]; }
    return 0;
}
static int pci_write_config_word(struct pci_dev *d, int pos, u16 value) {
    assert(pos==PCI_COMMAND); ++writes;
    if (write_fails) return -1;
    d->command=value; return 0;
}
static void msleep(unsigned ms) { ++sleeps; slept_ms+=ms; }
static void reset(void) {
    reads=writes=sleeps=slept_ms=bus_reads=next_status=0;
    memset(statuses,0,sizeof(statuses)); write_fails=false;
}
'''
MAIN = r'''
int main(void) {
    unsigned cap_cases=0, master_cases=0, pending_cases=0;
    /* Actual Xbox snapshot status has no capabilities-list bit. */
    struct pci_bus bus={.status=0x0288};
    for(unsigned type=0;type<256;type++) {
        reset(); bus.status=0x0288;
        assert(__pci_bus_find_cap_start(&bus,0,type)==0 && bus_reads==1);
        reset(); bus.status=0x0298;
        u8 expected=type<2?PCI_CAPABILITY_LIST:(type==2?PCI_CB_CAPABILITY_LIST:0);
        assert(__pci_bus_find_cap_start(&bus,0,type)==expected && bus_reads==1);
        cap_cases+=2;
    }
    const u16 commands[]={0,2,4,6,0x100,0x104,0xfffb,0xffff};
    for(unsigned i=0;i<sizeof(commands)/sizeof(commands[0]);i++)
    for(unsigned fail=0;fail<2;fail++) {
        reset();write_fails=fail;
        struct pci_dev dev={.is_busmaster=true,.command=commands[i]};
        pci_clear_master(&dev);
        assert(reads==1 && writes==!!(commands[i]&PCI_COMMAND_MASTER));
        assert(!dev.is_busmaster && !sleeps);
        assert(dev.command==(fail?commands[i]:(commands[i]&~PCI_COMMAND_MASTER)));
        ++master_cases;
    }
    /* Non-PCIe reports success without reading, sleeping, or clearing master. */
    reset();struct pci_dev dev={.pcie_cap=0,.command=6,.is_busmaster=true};
    assert(pci_wait_for_pending_transaction(&dev)==1);
    assert(!reads && !writes && !sleeps && dev.command==6 && dev.is_busmaster);
    ++pending_cases;
    /* PCIe bit clears at each possible observation, or never clears. */
    for(unsigned clear_at=0;clear_at<=4;clear_at++) {
        reset();dev.pcie_cap=0x40;
        for(unsigned i=0;i<4;i++) statuses[i]=i<clear_at?PCI_EXP_DEVSTA_TRPND:0;
        int result=pci_wait_for_pending_transaction(&dev);
        unsigned count=clear_at<4?clear_at+1:4;
        unsigned waits=count-1;
        assert(result==(clear_at<4));assert(reads==count && sleeps==waits);
        assert(slept_ms==((1u<<waits)-1u)*100u && !writes);
        assert(dev.command==6); ++pending_cases;
    }
    /* A failed command write is not reported by this void helper. */
    reset();dev=(struct pci_dev){.pcie_cap=0,.command=6,.is_busmaster=true};
    write_fails=true;pci_clear_master(&dev);
    assert(!dev.is_busmaster && dev.command==6 && writes==1);
    assert(pci_wait_for_pending_transaction(&dev)==1 && reads==1);
    printf("{\"capability_start_cases\":%u,\"clear_master_cases\":%u,"
           "\"pending_cases\":%u,\"failed_write_then_successful_wait\":true,"
           "\"non_pcie_success_reads\":0,\"max_simulated_sleep_ms\":700}\n",
           cap_cases,master_cases,pending_cases);
    return 0;
}
'''


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kernel',required=True,type=Path)
    parser.add_argument('--header-capture',required=True,type=Path)
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args()
    if args.output.exists():
        parser.error('Output exists; preserve prior evidence')
    pci=args.kernel/'drivers/pci/pci.c'; header=args.kernel/'include/linux/pci.h'
    sources={}
    for name in ['pci_pcie_cap','pci_is_pcie']:
        sources[name]=extract(header.read_text(),name)
    for name in ['__pci_bus_find_cap_start','__pci_set_master','pci_clear_master',
                 'pci_wait_for_pending','pci_wait_for_pending_transaction']:
        sources[name]=extract(pci.read_text(),name)
    capture=json.loads(args.header_capture.read_text())
    raw=bytes.fromhex(capture.get('pci_config_header_hex',capture.get('pci_header_hex','')))
    if len(raw)!=64 or raw[:4]!=bytes.fromhex('14140c58'):
        raise ValueError('Expected an exact 64-byte header for 1414:580c')
    status=int.from_bytes(raw[6:8],'little')
    with tempfile.TemporaryDirectory(prefix='obsidian-pci-contract-') as temp:
        temp=Path(temp); source=temp/'test.c'; binary=temp/'test'
        source.write_text(PREFIX+'\n'.join(sources.values())+MAIN)
        subprocess.run(['clang','-std=c11','-O1','-Wall','-Wextra','-Werror',
                        '-fsanitize=address,undefined',str(source),'-o',str(binary)],check=True)
        result=subprocess.run([str(binary)],capture_output=True,text=True,check=True)
        if result.stderr:
            raise RuntimeError(result.stderr)
    report={'passed':True,'scope':'Seven actual Linux PCI functions; configuration and delays mocked. No hardware writes.',
            'source_sha256':{str(p.relative_to(args.kernel)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [pci,header]},
            'function_sha256':{name:hashlib.sha256(s.encode()).hexdigest() for name,s in sources.items()},
            'capture_sha256':hashlib.sha256(args.header_capture.read_bytes()).hexdigest(),
            'capture_observed_utc':capture.get('captured_utc',capture.get('console_observed_utc')),
            'decoded_header':{'vendor':'1414','device':'580c','command':int.from_bytes(raw[4:6],'little'),
                              'status':status,'header_type':raw[14]&0x7f,
                              'capabilities_list_advertised':bool(status&16),'capability_pointer_byte':raw[52]},
            'tests':json.loads(result.stdout),'sanitizers':'ASan/UBSan',
            'limitations':['Snapshot decoding is historical unless freshly captured.',
                          'No proof of outstanding DMA completion, reset success, or endpoint electrical behavior.',
                          'PCI capability absence is inferred from the header and standard enumeration; no live kernel struct was read.']}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
