def get_unlabeled_families():
    label_me = []
    with open('google-fonts.json') as json_file:
        gfData = json.load(json_file)
        fontlist = gfData['items']

        for font in fontlist:
            is_serif = check_if_serif(family.lower(),category)

            # Add families with is_serif = -1 to list of families to label by hand
            if is_serif == -1:
                # print(family)
                # is_serif = input(family + ' is_serif: ')
                label_me.append(family)

    # Write contents of label_me list to file
    with open('label_me.txt', 'w') as filehandle:
        for f in label_me:
            filehandle.write('%s\n' % f)
    # print(label_me)
    # f = open("label_me.txt", "w")
    # f.write(label_me)
    # f.close()