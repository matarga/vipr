---
Title: "VIPER"
Author: "Matias Argandona AKA Goog07,Goog-hash,Goog-yaml"
Description: "small side project to create the smallest meshtastic node system with multiple models ranging from large TX mast powerhouses to tiny iPod sized mobile nodes capable of running any open source large radio firmware"
Created_at: "2026-07-04"
---

# July 6th: Second revision

Today I redid the board again, following my normal routine redo to get the size smaller and smaller.

Rev1 was large and rev1.1 adopted a stick like shape while rev1.2 got wider by around 2 mm but a lot shorter.  

![revision1](viperv1.png)<br>
As seen here Revision one is very big, with that LiPo holder on board a lot of the footprint is dedicated to that and that only. Making it very clunky for it's intended purpose.  

![revision1.1](viperv1.1.png)<br>
Revision 1.1 fixes this by adding a two pin JST connector to save space with the added complexity of now needing to find the correct battery and tuning the board for it. And also the extra connectors adds more complexity requiring another component to be on the edge.  <br>

![revision1.2](viperv1.2.png)<br>
Revision 1.2 fixes the issue of the USB serial chip and mitigates a possible manufacturing issue considering the chip used (FTDI FT231XQ) is outdated and expesive. To combat this I replaced the old IC with a new CH340X that has less pins and an arguably easier to work with MSOP-10 package. The package does come with gullwing pins, now most people would think of this as a size increase but considering my (questionable) soldering skills I consider it a pro.  

So far the project seems to be going good, I think I'm going to split this repo for different models of VIPER. See you!  

-Matias =)

[Total time spent: 48 mins]

# July 22nd: Brushing dust off this

I'm running up to add an addon system for the device and some dedicated pins to do so. as getting this from another really cool project called pocketbyte, go check it out!

I changed all of the LEDs to soft switches instead because i felt it looked nice.

I'm currently going to source a ref for the pinout soon. But It's going good.

- Matias

# July 28th

I just finished rev2 for the board! What's new?

I fixed the issue of all the passive components being 0402 metric then I decided to learn about hwo to pick the correct sizes for each component.

The CH340X is back in the board to allow USB serial and I'm thinking about adding JTAG headers to the board for debugging.

I went back to the pen form factor and also am considering adding a screen to the board.

There will be not more motive changes for now and the project will stay like this.

I'm going to continue to work on this and I think I'm going to get this produced

# July 30th: Added a screen and mounting holes

For revision 2.1. I introduced a versioning system of major and minor.
 What's new in 2.1?

Mounting holes for M2 screws on the left side of the board and a header connection for a screen. the schematics now include test points for serial, power, and JTAG soon to be onboard for revision 2.2.

Some issues were included in revision 2 that would prevent stable operation of the radio caused by a faulty connection between the regulator for the SX1262 and the inductor managing it.

That's all.

-Matias

# Aug 5th: Revision 3

Currently the schematic is updated to have an SD Card, a neopixel LED, and a DPAD to make sure the final is a functioning prototype. Also the schematic has been sorted out into boxes per each component. Good.

-Matias

# Sep 5th: A rebirth to a dying project.

I've not been able to work on this project for almost a month now because of school but now I can work weekends whenever possible. You may ask: "What's new"?. For starters, I've added a ton of stuff to the schematic, the device has adopted a RPI02W form factor of 30mm by 65 mm and M2.5 mounting screws. So far, I've repositoned the battery connecter and am working on transfering components to the new board, I have a problem though... the battery connector is way too big to fit under the display (curse you 2 pin JST). I'm looking on LCSC for identical connectors to the device capable of 5V and 1A loads. Im don't know how I''m going to solve it for now but I know for a fact it will be done, I'm trying to achive the pwnagatchi form factor (a long dead device) making updates hourly.

-Matias
