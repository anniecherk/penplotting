activate:
    source venv/bin/activate


gen_star_field:
    vsk run star_field

# vpype read test-fancy-thick-spline.svg  linemerge cfill -t 1mm -pw .1mm show
# vpype read test-fancy-thick-spline.svg  linemerge cfill -t 1mm -pw .3mm scale 0.3 0.3 show

gcode input:
    #!/usr/bin/env bash
    set -euxo pipefail
    vpype --config config.toml \
        read {{input}} \
        linemerge \
        cfill --tolerance 1mm --pen-width 0.1mm \
        linesimplify --tolerance 0.01mm \
        linesort \
        gwrite {{input}}.gcode \
        show
        
vsketch:
    vsk run first_vsketch_project/


full_flower:
    vpype --config config.toml read flower_watercolor/stamen.svg penwidth 1mm linemerge linesimplify layout --fit-to-margins 3in 9inx12in translate 1.75in -2.25in rect 0.5in 0.5in 8in 11in rect 1.25in 9.25in 1.25in 1.25in rect 1.25in 7.5in 1.25in 1.25in gwrite flower.gcode

# smol_flower

#gcode input:
#    #!/usr/bin/env bash
#    set -euxo pipefail
#    vpype --config config.toml \
#        read {{input}} \
#        linemerge \
#        cfill --tolerance 1mm --pen-width 0.3mm \
##        scale 0.3 0.3 \
#        linesimplify --tolerance 0.01mm \
#        gwrite {{input}}.gcode \
#        show
        
        
        
#  
# --tolerance 0.01mm \
#linesort \
#reloop \
#linesimplify --tolerance 0.01mm \