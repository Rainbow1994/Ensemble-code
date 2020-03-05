def decode_line(line, separator=' '):
    line=line.strip()
    line.replace('\n', '')
    schar=""
    terms=list()
    item=""
    for schar in line:
        if (schar==separator):
            if (len(item)>0):
                terms.append(item)
                item=""
            else:
                item=""
        else:
            item=item+schar
            

    if (len(item)>0):
        terms.append(item)
        
    return terms
