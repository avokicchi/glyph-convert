from PIL import Image
import os, sys, getopt
from pathlib import Path

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print ('convert.py -i <inputfile> -o <outputfile>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print ('convert.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    if inputfile == '':
        print ('convert.py -i <inputfile> -o <outputfile>')
        sys.exit(2)

    if outputfile == '':
        outputfile = Path(inputfile).stem + ".txt"

    image = Image.open(inputfile)
    # Ensure it's in RGBA mode
    image = image.convert('RGBA')
    pixels = image.load()

    t = pixels[0, 0]#topleft pixel is "background". dumb, but works often

    if os.path.exists(outputfile):
        answer = input("outputfile " + outputfile+ " exists, overwrite? y/n")
        if answer.lower() == "y":
            os.remove("out.txt")
        elif answer.lower() == "n":
            sys.exit(2)
        else: 
            sys.exit(2)

    print(outputfile)

    with open(outputfile, "a", encoding="utf-8") as file:

        # Loop through all pixels in steps of 2
        width, height = image.size
        for y in range(0,height,2):
            for x in range(0,width,2):
                tl = False
                tr = False
                bl = False
                br = False
                r, g, b, a = pixels[x, y]
                tl = not (r == t[0] and g == t[1] and b == t[2] and a == t[3])
                if y+1<height:#there is room below (handling edges):
                    r, g, b, a = pixels[x, y + 1]
                    bl = not (r == t[0] and g == t[1] and b == t[2] and a == t[3])
                else:
                    bl = False
                if x+1<width:# there is room on the right:
                    r, g, b, a = pixels[x + 1, y]
                    tr = not (r == t[0] and g == t[1] and b == t[2] and a == t[3])
                else:
                    tr = False
                if x+1<width and y+1<height:#there is room on the right and there is room below:
                    r, g, b, a = pixels[x + 1, y + 1]
                    br = not (r == t[0] and g == t[1] and b == t[2] and a == t[3])
                else:
                    br = False

                if tl and not tr and not bl and not br:
                    #single topleft pixel
                    file.write(chr(0x2598))
                elif not tl and tr and not bl and not br:
                    #single topright pixel
                    file.write(chr(0x259D))
                elif not tl and not tr and not bl and not br:
                    #space
                    file.write(chr(0x0020))
                elif tl and not tr and not bl and br:
                    #topleft to bottomright line
                    file.write(chr(0x259A))
                elif bl and tr and not br and not tl:
                    #bottomleft to topright line
                    file.write(chr(0x259E))
                elif bl and not br and not tl and not tr:
                    #bottomleft pixel
                    file.write(chr(0x2596))
                elif not tl and not tr and not bl and br:
                    #bottomright pixel
                    file.write(chr(0x2597))
                elif tl and bl and not tr and not br:
                    #left line
                    file.write(chr(0x258C))       
                elif tl and tr and not bl and not br:
                    #top line
                    file.write(chr(0x2580))
                    #file.write(chr(0x2580))
                elif not tl and not bl and tr and br:
                    #right line
                    file.write(chr(0x2590))       
                elif not tl and bl and not tr and br:
                    #bottom line
                    file.write(chr(0x2584))          
                elif tl and not tr and bl and br:
                    #everything except tr
                    file.write(chr(0x2599))          
                elif tl and tr and bl and not br:
                    #everything except br
                    file.write(chr(0x259B))          
                elif tl and tr and not bl and br:
                    #everything except bl
                    file.write(chr(0x259C))                       
                elif not tl and tr and bl and br:
                    #everything except tl
                    file.write(chr(0x259F))         
                elif tl and tr and bl and br:
                    #FULL BLOCK
                    file.write(chr(0x2588))                                    

            file.write("\n")

if __name__ == "__main__":
    main(sys.argv[1:])