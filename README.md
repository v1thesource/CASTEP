# CASTEP
Little programs that help with data manipulation of files in the CASTEP density functional theory code.

Objectives: 1) Speed up the slowest parts of post-processing DFT outputs
            2) Maintain and improve old scripts for manipulating data
            3) Automate ourselves out of a job

# Brouwer Diagrams

Currently, the sensitivity_analysis script outputs many different plots which need 
to be joined together. Thankfully, we have a brew package called imagemagick which
stitches together multiple images to create gifs, with lots of custom options.

First, get imagemagick with brew (I use OSX) with:

brew install imagemagick

Then, pass all your files into the 'convert' function. Here's an example of tet
Brouwer diagrams with a 0.03 second delay per frame:

convert -delay 3 -verbose -loop 0 tet_brouwer{300..2500..5}.png myimage-tet.gif


