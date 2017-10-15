import os

files = os.listdir()

for image in files:
    if image[-3:] == "svg":
        svgname = image
        pdfname = svgname.replace("svg", "pdf").replace("_", "")
        cmd = "inkscape -D -z --file=%s --export-pdf=%s --export-latex" %(svgname, pdfname)
        os.system(cmd)
    else:
        print(image + " skipped.")

print("Done")