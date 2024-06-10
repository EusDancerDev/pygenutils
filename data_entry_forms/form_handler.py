#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

#-----------------------#
# Import custom modules #
#-----------------------#

# Define functions #
#------------------#

def verify_spanish_dni(dni):
    """
    Verify the validity of a Spanish DNI (Documento Nacional de Identidad).
    
    Parameters
    ----------

    dni : str
        The DNI (ID card) to be verified.
        
    Returns
    -------
    bool
        True if the DNI is valid, False otherwise.
    """
    if len(dni) != 9:
        return False

    digits = dni[:-1]
    control_letter = dni[-1].upper()

    if not digits.isdigit():
        return False

    letters = "TRWAGMYFPDXBNJZSQVHLCKE"
    calculated_letter = letters[int(digits) % 23]

    return calculated_letter == control_letter

