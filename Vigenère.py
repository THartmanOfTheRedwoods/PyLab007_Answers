#!/usr/bin/env python3
import sys


def vigenere_head(alphabet):
    alphabet = list( alphabet )
    print( f'| {' | '.join( [' '] + alphabet[0:] )} |' )
    print( f'{'|---' * (len( alphabet ) + 1)}|' )


def vigenere_sq(alphabet):
    vigenere_head( alphabet )
    alphabet = list( alphabet )
    for i in range( len( alphabet ) ):
        print( f'| {alphabet[i]} | {' | '.join( alphabet[i:] + alphabet[:i] )} |' )


def vigenere_sq_ok(alphabet):
    vigenere_head( alphabet )
    for i in range( len( alphabet ) ):
        row = '| '
        for l in alphabet:
            row += l + ' | '
        print( '| ' + alphabet[i] + ' ' + row )
        # Now shift the alphabet
        alphabet = alphabet[1:] + alphabet[0]


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


def encrypt_vigenere(key, plaintext, alphabet):
    cipher_text = ''
    key_len = len( key )
    for i, l in enumerate( plaintext ):
        cipher_text += vigenere_index( key[i % key_len], l, alphabet ) if l != ' ' else l
    return cipher_text


def undo_vigenere_index(key_letter, cypher_letter, alphabet):
    # print(f'{letter_to_index(cypher_letter, alphabet)} {letter_to_index(key_letter, alphabet)}')
    alpha_len = len(alphabet)
    return index_to_letter(
        ( letter_to_index( cypher_letter, alphabet ) -
          letter_to_index( key_letter, alphabet ) + alpha_len) % alpha_len, alphabet )


def decrypt_vigenere(key, cipher_text, alphabet):
    plaintext = ''
    key_len = len( key )
    for i, l in enumerate( cipher_text ):
        plaintext += undo_vigenere_index( key[i % key_len], l, alphabet ) if l != ' ' else l
    return plaintext


def main_menu():
    while True:
        print( """1). Encrypt
2). Decrypt
3). Quit""" )
        try:
            selected = int( input( "Make a selection:" ) )
            return selected if 0 < selected < 4 else 3
        except ValueError:
            print( "Improper selection, please press 1, 2, or 3" )


def enc_menu(key, alphabet):
    plaintext = input( "Enter the text you'd like to encrypt: " )
    return encrypt_vigenere( key, plaintext, alphabet )


def dec_menu(key, alphabet):
    ciphertext = input( "Enter the cipher text you'd like to decrypt: " )
    return decrypt_vigenere( key, ciphertext, alphabet )


def main():
    # vigenere_sq(alphabet)
    key = 'DAVINCI'
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    result = ''
    while True:
        match (main_menu()):
            case 1:
                result = enc_menu( key, alphabet )
            case 2:
                result = dec_menu( key, alphabet )
            case 3:
                sys.exit( 0 )

        print( result )


if __name__ == '__main__':
    main()