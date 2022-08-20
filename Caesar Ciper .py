from turtle import position


alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 
'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
 'x', 'y', 'z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 
 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n")
text = input("Type your message:\n").lower()
shift = int(input("Type the shift number:\n"))

def caesar(start_text,shift_amount,direction_Off):
       end_text =""
       for letter in start_text:
        position = alphabet.index(letter)
        if direction_Off == "decode":
             shift_amount = shift_amount * -1
             new_position = position + shift_amount
             end_text += alphabet[new_position]
       print(f"the {direction_Off}d text is {end_text}") 

caesar(text , shift,direction)     
      

#def encrypt(plain_text ,shift_amount):
 #   cipher_text = " "
  #  for letter in plain_text:
   #  position = alphabet.index(letter)
    # new_position = position + shift_amount
    # new_letter = alphabet[new_position]
    # cipher_text += new_letter
   # print(f"The Encoded text is {cipher_text}")

#def decrypt(cipher_text ,shift_amount):
 #   plane_text = " "
  #  for letter in cipher_text:
   #  position = alphabet.index(letter)
   #  new_position = position - shift_amount
    # new_letter = alphabet[new_position]
    # plane_text += new_letter
   # print(f"The decoded text is {plane_text}")


     
#if direction == "encode" :
 #   encrypt(text ,shift) 
#elif direction=="decode" :
 #   decrypt(text ,shift) 