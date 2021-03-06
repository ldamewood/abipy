"""
generate the rst files for the examples by iterating over the abipy examples
"""
# Taken from matplotlib
import os, glob
import re
import sys

fileList = []

def out_of_date(original, derived):
    """
    Returns True if derivative is out-of-date wrt original,
    both of which are full file paths.

    TODO: this check isn't adequate in some cases.  Eg, if we discover
    a bug when building the examples, the original and derived will be
    unchanged but we still want to force a rebuild.
    """
    return (not os.path.exists(derived) or
            os.stat(derived).st_mtime < os.stat(original).st_mtime)

noplot_regex = re.compile(r"#\s*-\*-\s*noplot\s*-\*-")

def generate_example_rst(app):
    head, tail = os.path.split(app.builder.srcdir)
    rootdir = os.path.join(head, "abipy", "examples")
    exampledir = os.path.join(app.builder.srcdir, 'examples')
    #print(head, rootdir, exampledir)

    if not os.path.exists(exampledir): 
        os.makedirs(exampledir)

    datad = {}
    for root, subFolders, files in os.walk(rootdir):
        for fname in files:
            if ( fname.startswith('.') or fname.startswith('#')
                 or fname.startswith('_') or not fname.endswith('.py') ): continue

            fullpath = os.path.join(root,fname)
            with open(fullpath, "r") as f:
                contents = f.read()
            # indent
            relpath = os.path.split(root)[-1]
            datad.setdefault(relpath, []).append((fullpath, fname, contents))

    subdirs = sorted(datad.keys())
    #subdirs.sort()

    fhindex = open(os.path.join(exampledir, 'index.rst'), 'w')

    fhindex.write("""\
.. _examples-index:

##############
Abipy Examples
##############

.. htmlonly::

    :Release: |version|
    :Date: |today|

.. toctree::
    :maxdepth: 2

""")

    for subdir in subdirs:
        rstdir = os.path.join(exampledir, subdir)
        if not os.path.exists(rstdir):
            os.makedirs(rstdir)

        outputdir = os.path.join(app.builder.outdir, 'examples')
        if not os.path.exists(outputdir):
            os.makedirs(outputdir)

        outputdir = os.path.join(outputdir, subdir)
        if not os.path.exists(outputdir):
            os.makedirs(outputdir)

        subdirIndexFile = os.path.join(rstdir, 'index.rst')
        fhsubdirIndex = open(subdirIndexFile, 'w')
        fhindex.write('    %s/index.rst\n\n'%subdir)

        fhsubdirIndex.write("""\
.. _%s-examples-index:

##############################################
%s Examples
##############################################

.. htmlonly::

    :Release: |version|
    :Date: |today|

.. toctree::
    :maxdepth: 1

"""%(subdir, subdir))

        #sys.stdout.write(subdir + ", ")
        #sys.stdout.flush()

        data = datad[subdir]
        data.sort()

        for fullpath, fname, contents in data:
            basename, ext = os.path.splitext(fname)
            outputfile = os.path.join(outputdir, fname)
            #thumbfile = os.path.join(thumb_dir, '%s.png'%basename)
            #print '    static_dir=%s, basename=%s, fullpath=%s, fname=%s, thumb_dir=%s, thumbfile=%s'%(static_dir, basename, fullpath, fname, thumb_dir, thumbfile)

            rstfile = '%s.rst'%basename
            outrstfile = os.path.join(rstdir, rstfile)

            fhsubdirIndex.write('    %s <%s>\n'%(os.path.basename(basename),rstfile))

            if not out_of_date(fullpath, outrstfile): continue

            fh = open(outrstfile, 'w')
            fh.write('.. _%s-%s:\n\n'%(subdir, basename))
            title = '%s example code: %s'%(subdir, fname)
            #title = '<img src=%s> %s example code: %s'%(thumbfile, subdir, fname)

            fh.write(title + '\n')
            fh.write('='*len(title) + '\n\n')

            do_plot = (subdir in ['plot',] and
                       not noplot_regex.search(contents))

            do_autorun = subdir in ["htc",] #and not noautorun_regex.search(contents))

            #sys.stderr.write("subdir %s, full_path %s\n" % (subdir, fullpath))

            if do_plot:
                fh.write("\n\n.. plot:: %s\n\n::\n\n" % fullpath)

            elif do_autorun:
                #sys.stderr.write("in autorun with %s" % fullpath)
                fh.write("\n\n.. runblock:: pycon\n\n")
                # Autorun requires >>> at the beginning of the line.
                contents = '\n'.join(['>>> %s'% row.rstrip() for row in contents.split('\n')])


            else:
                fh.write("[`source code <%s>`_]\n\n::\n\n" % fname)
                fhstatic = open(outputfile, 'w')
                fhstatic.write(contents)
                fhstatic.close()

            # indent the contents
            contents = '\n'.join(['    %s'%row.rstrip() for row in contents.split('\n')])

            fh.write(contents)
            fh.close()

        fhsubdirIndex.close()

    fhindex.close()
    print("")

def setup(app):
    app.connect('builder-inited', generate_example_rst)
