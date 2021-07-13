from PIL import Image
import itertools as it
import string as s

# Build map of character to atlas index
char_sequence = it.chain(
    s.ascii_lowercase, s.ascii_uppercase, s.digits, ".,!?:;|'\"&()<>[]{}=+-*/\\%#$@"
)
char_map = {c: i for i, c in enumerate(char_sequence)}
char_map[" "] = 255

# read in atlas
atlas = Image.open("modified_petscii_8x8.png")

# create output terminal image
term = Image.new("RGB", (640, 480))
text = """
                               Brady W Burnsides

     US Citizen     |   137 Williams Pointe Blvd SW  |   brady@burnsides.us
  Secret Clearance  |      Huntsville, AL 35824      |     (423) 290-2269
  -------------------------------------------------------------------------

     EDUCATION ------------------------------------------------------------
     Master of Science in Software Engineering         Expected: May 2026
     University of Alabama in Huntsville
        - Concentration: Software Engineering / Project Management
        - Status: Completing undergraduate breadth requirements for
        graduate program admission
     Bachelor of Science in Aerospace Engineering   Conferred: April 2020
     University of Alabama in Huntsville
        - Honors: Magna cum laude (GPA: 3.50 / 4.00)
        - Minors: Mathematics

     SKILLS ----------------------------------------------------------------
     - Python, C, C++, C#, Java
     - Git version control
     - Windows, Linux, macOS
     - Word Processing with Word and LaTeX
     - Technical research, writing, presentation
     - Digital logic design and prototyping
     - Teledyne Brown Engineering's OSC

     PROJECTS --------------------------------------------------------------
     - Link margin budget development for multi-stage mission to Venus
     - Design, prototyping, PCB fabrication, and software development
     for homebrew 8-bit CPU and peripherals from scratch, using
     TTL digital logic chips.
     - Python RPG development using custom event-driven framework

     EXPERIENCE ------------------------------------------------------------
     Aerospace Threat Modeling Engineer               June 2021 - Present
     Parsons Corporation                                   Huntsville, AL

     Research Engineer                                May 2020 - May 2021
     Previous: Research Assistant                February 2020 - May 2020
     UAH Research Institute                                Huntsville, AL

     Researcher                             November 2019 - February 2020
     Noetic Strategies                                     Huntsville, AL

     Engineering Intern                        August 2019 - January 2020
     UAH Propulsion Research Center                        Huntsville, AL

     Museum Associate                           May 2018 - September 2019
     US Space & Rocket Center                              Huntsville, AL

"""

cursor = [0, 0]
in_escape = False
escape_buffer = []
for c in text:
    if c == "\n":
        cursor[0] = 0
        cursor[1] += 1
        continue
    if c == "\b":
        cursor[0] -= 1
        continue
    if c == "\r":
        cursor[0] = 0
        continue
    if c == "\t":
        cursor[0] += 4
        continue

    try:
        idx = char_map[c]
    except KeyError:
        idx = 143
    x, y = idx // 16, idx % 16
    left = y * 8
    top = x * 8
    im = atlas.crop((left, top, left + 8, top + 8))

    # paste image onto term
    term.paste(im, (cursor[0] * 8, cursor[1] * 8))

    cursor[0] += 1
    if cursor[0] == 80:
        cursor[0] = 0
        cursor[1] += 1

        if cursor[1] == 60:
            cursor[1] == 0

    # break

term.save("emulated_terminal.png")
