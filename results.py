def filter_result(scansioni, filter_selector):
        
        if filter_selector == 2:
            porte_aperte = []    
            for scansione in scansioni:
                if scansione.is_open():
                    porte_aperte.append(scansione)
            return porte_aperte
        elif filter_selector == 3:
            porte_chiuse = []
            for scansione in scansioni:
                if scansione.is_closed():
                    porte_chiuse.append(scansione)
            return porte_chiuse
        elif filter_selector == 4:
            errori = []
            for scansione in scansioni:
                if scansione.has_error():
                    errori.append(scansione)
            return errori
        else:
            return scansioni

def statistiche(scansioni):
    
    porte_aperte = 0
    porte_chiuse = 0
    errori = 0
    porte_scansionate = 0

    for scansione in scansioni:
        porte_scansionate += 1
        if scansione.is_open():
            porte_aperte +=1
        elif scansione.is_closed():
            porte_chiuse += 1
        else:
            errori +=1
    
    return {
        "porte_scansionate": porte_scansionate,
        "porte_aperte": porte_aperte,
        "porte_chiuse": porte_chiuse,
        "errori": errori
    }