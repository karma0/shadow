=====
Usage
=====

To use Shadow in a project::

    from shadow.shadow import Shadow
    shadow = Shadow()
    for tmpl in shadow.run():
        print(f"Generating template--source: {tmpl.source}; destination: {tmpl.destination}")
    shadow.render()

To use Shadow on the command line, consult the output of the following command::

   shadow --help
