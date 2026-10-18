![banner](banner.png)

# What is VIPR?

Simply put, VIPR is a open source radio node designed and built around North American mesh communication over LoRa built off of an ESP32-S3 platform. Put less simply, VIPR is another ESP32 development board focused more on frontend, hardware, and size. The project aims to create a small, pocketable radio node that can run independently. Currently the procsessing power of it's latest version (2.0) can only handle small workloads and can only run a Real Time OS in comparison to a fully fledged computer.

**VIPR is currently in Alpha testing, soon to be beta!**

I'm planning on spinning this project idea and base into another, thinking aboutthe name of ProtopadZero

## Current Revision

![Render1](main.png)

Currently the board packs a 19mm wide footprint without a screen. The end is equipped with an SMA conector for easy antenna swaps and the side boasts an onboard PCB wifi antenna tied to the ESP32-MINI-1 module.

Future revisions intend to add a screen and interactives to the board to further refine the frontend, all that is needed after that is software and a case!

### Changelog

```
* Redid a proper BOM
    * This included sizing and components selection
* Added back the CH340X
* Reverted to old "pen" form factor
* Created a new "lopsided" board end 
* Added a screen header
* Fixed a regulator issue on the radio portion
* bundled CAD files into production folders <=2.1
* Added JTAG test pads for rev 2.1.1
```

## Docs

Docs will be coming soon!
<br>

## Versioning system

The project follows a versioning system of major and minor. The first number in the version is the board platform. Whenever the board is fully redone a new major version will be released. Whenever the board has a small tweak to an existing platform version the second number behind the first will be bumped up by one.

A board version of say, 2.1 would indicate platform version 2 with one tweak of the original version 2.0.

#### Latest Journal as of July 28th

For revision 2.1. I introduced a versioning system of major and minor.
 What's new in 2.1?

Mounting holes for M2 screws on the left side of the board and a header connection for a screen. the schematics now include test points for serial, power, and JTAG soon to be onboard for revision 2.2.

Some issues were included in revision 2 that would prevent stable operation of the radio caused by a faulty connection between the regulator for the SX1262 and the inductor managing it.

That's all.

-Matias
