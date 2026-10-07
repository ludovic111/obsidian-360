# Physical actions and external dependencies

The user returned on October 2 and completed the **obsidian_clock** boot. E73 verifies the kernel and clock correction; the user confirms desktop responsiveness. That boot action is no longer blocked. Physical actions below still require coordination, and no unattended reboot is assumed authorized merely because SSH is available.

| Action | Why it is needed | Independent work available |
|---|---|---|
| Test Shut Down from the normally launched desktop | Real-process authorization was checked, but successful poweroff was not observed | Session/authorization analysis and host tests |
| Visually identify motherboard and chip markings | PCI signatures do not establish every revision | Driver analysis and logical memory map |
| Test Big Order on another known-working DVD player | CD samples read, game/video DVDs absent in Linux and reportedly in stock dashboard | SCSI/sense analysis and software-format tooling |
| Exercise controller pointer, A/Y, keyboard, and repeated window resize | General responsiveness is confirmed, but not every gesture or resize recovery | Launcher tests and X11 instrumentation |
| Repeat explicit candidate boot and return to the previous kernel | One clock-kernel boot is verified; fallback files alone do not demonstrate a fresh rollback | Initramfs, menu, source, and timing analysis |
| Establish hardware-appropriate NAND recovery | No confirmed restorable raw backup or independent recovery chain | Acquisition source review, image/ECC format analysis, synthetic tests |

The optical drive is not declared repaired, and successful game reading has not been demonstrated. Game research uses documented formats and synthetic fixtures until a usable legitimately owned input is available locally.

A pending physical step does not block all research. Continue a genuinely independent source, tooling, testing, or documentation task and preserve the exact outstanding action here.
