#!/usr/bin/env python3
import sys


def vigenere_head(alphabet):
    return [list(list(' ') + list( alphabet ))]


def vigenere_sq(alphabet):
    alphabet = list( alphabet )
    sq_list = vigenere_head( alphabet )
    for i in range( len( alphabet ) ):
        sq_list.append(list(alphabet[i]) + alphabet[i:] + alphabet[:i])
    return sq_list


def vigenere_sq_print(sq_list):
    for i, row in enumerate(sq_list):
        print( f'| {' | '.join( row[0:] )} |' )
        if i == 0:
            print( f'{'|---' * (len( row ))}|' )


def vigenere(alphabet):
    vigenere_sq_print(vigenere_sq(alphabet))


def letter_to_index(letter, alphabet):
    return alphabet.upper().find( letter.upper() )


def index_to_letter(index, alphabet):
    if 0 <= index < len( alphabet ):
        return alphabet[index].upper()
    return None


def vigenere_index(key_letter, plaintext_letter, alphabet):
    return index_to_letter(
        (letter_to_index( plaintext_letter, alphabet ) +
         letter_to_index( key_letter, alphabet )) % len( alphabet ), alphabet )


def undo_vigenere_index(key_letter, cypher_letter, alphabet):
    # print(f'{letter_to_index(cypher_letter, alphabet)} {letter_to_index(key_letter, alphabet)}')
    alpha_len = len(alphabet)
    return index_to_letter(
        ( letter_to_index( cypher_letter, alphabet ) -
          letter_to_index( key_letter, alphabet ) + alpha_len) % alpha_len, alphabet )


def encrypt_vigenere(key, plaintext, alphabet):
    cipher_text = []
    key_len = len( key )
    for i, l in enumerate( plaintext ):
        cipher_text.append(vigenere_index( key[i % key_len], l, alphabet ) if l != ' ' else l)
    return ''.join(cipher_text)


def decrypt_vigenere(key, cipher_text, alphabet):
    plaintext = []
    key_len = len( key )
    for i, l in enumerate( cipher_text ):
        plaintext.append(undo_vigenere_index( key[i % key_len], l, alphabet ) if l != ' ' else l)
    return ''.join(plaintext)


def execute(menu, skip):
    while True:
        for i in range(len(menu) - skip):
            print( menu[i][0] )
        try:
            selected = int( input( "Make a selection: " + str(menu[-1]) ) )
            if selected in menu[-1]:  # If selected is in valid options.
                selected -= 1  # Shift index back to 0 based.
                # First let's make sure a function object exists, and return if it doesn't
                if menu[selected][1] is None:  # Assume it's a quit
                    return
                if menu[selected][3] is not None:  # If there is a return list defined.
                    menu[selected][3].append(menu[selected][1](*menu[selected][2]))
                else:  # Just all the function object otherwise.
                    menu[selected][1](*menu[selected][2])
            else:
                raise ValueError
        except ValueError:
            print( "Improper selection. You must select one of: " + str(menu[-1]) )


def enc_menu(key_list, encrypted_list, alphabet):
    plaintext = input( "Enter the text you'd like to encrypt: " )
    key_index = len(encrypted_list) % len(key_list)
    return encrypt_vigenere( key_list[key_index], plaintext, alphabet )


def dec_menu(key_list, encrypted_list, alphabet):
    key_len = len(key_list)
    for i, ciphertext in enumerate(encrypted_list):
        key_index = i % key_len
        print(decrypt_vigenere( key_list[key_index], ciphertext, alphabet ))


def dec_dump_menu(encrypted_list):
    for ciphertext in encrypted_list:
        print(ciphertext)

def key_entry(alphabet, key_list):
    how_many_keys = int( input( "How many keys are you going ot enter? "))
    for _ in range(how_many_keys):
        key = input( "Please enter a key: ")
        # TODO: Remove any key characters not in alphabet
        key_list.append(key)

def main():
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    encrypted_list = []
    key_list = []

    # Each Row is: 'menu-item', 'function object', 'function parameters', 'return list'
    key_menu = [
        ['1). Enter Keys', key_entry, [alphabet, key_list], None],
        ['2). Quit', None, [0], None],
        [1, 2]  # Valid options
    ]
    execute(key_menu, 1)

    menu = [
        ['1). Encrypt', enc_menu, [key_list, encrypted_list, alphabet], encrypted_list],
        ['2). Decrypt', dec_menu, [key_list, encrypted_list, alphabet], None],
        ['3). Dump Decrypt', dec_dump_menu, [encrypted_list], None],
        ['4). Vigenère Square ', vigenere, [alphabet], None],
        ['5). Quit', sys.exit, [0], None],
        [1, 2, 3, 4, 5]  # Valid options
    ]
    execute(menu, 1)


if __name__ == '__main__':
    main()