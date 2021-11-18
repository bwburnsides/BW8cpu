# BW8cpu

An 8-bit processor and peripherials from first principles.

    If you wish to make apple pie from scratch, you must first create the universe.
                                                    -- Carl Sagan

---

My project is inspired by Ben Eater's [8 bit breadboard computer](https://eater.net/8bit), and his follow-on series with the [6502 processor](https://eater.net/6502) and a home-built [VGA video card](https://eater.net/vga). I hope to bridge the gap between these series by developing a CPU that is similar enough in capability to the 6502, that the video card and other peripherials (eg, PS/2 keyboard) can directly interface with the device. Since its inception, the project scope has advanced significantly. Now, there are plans for a wider set of peripherals that will transform the CPU into a full fledged computer.

Heavy architecture inspirations also comes from James Sharman's [8 bit homebrew pipelined CPU](https://www.youtube.com/c/weirdboyjim/videos) project, though mine is not pipelined.

Ultimately, the programming model is similar to that of the [Motorola 6809](https://en.wikipedia.org/wiki/Motorola_6809), or more specifically, the [Hitachi 6309](https://en.wikipedia.org/wiki/Hitachi_6309).

## Architecture Overview

![architecture diagram of cpu](docs/arch_diagram.png)

## Dev Log

I'll be updating a dev log with the source files found in `dev-log/`. Here are the most recent posts:

- [001 Initial Planning](dev-log/001-initial-planning.md)
- [002 Memory Map Planning](dev-log/002-memory-map-planning.md)
- [003 VGA Planning](dev-log/003-vga-planning.md)