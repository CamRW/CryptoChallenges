import base64
import binascii
import codecs
import bitstring

def base64_to_hex(h):
    
    bin_str = base64.b64decode(h.encode('utf8'))
    
    return binascii.hexlify(bin_str).decode('utf8')

def hex_to_base64(h):

	if ((len(h) % 4) != 0):
		return 'String must be divisible by 4'
	else:
		hexi = codecs.decode(h,'hex')

		print(hexi)
		base64_out = base64.b64encode(hexi)

		return base64_out

def fixed_xor(str_1,str_2):

	result = BitArray()

	for lb, rb in zip(str_1.cut(8), str_2.cut(8)):
		result += lb ^ rb
	
	return result

def xor_cipher_break(data):
	decoded = codecs.decode(data,'hex')
	key = max(decoded, key=decoded.count) ^ ord(' ')
	result = ''.join(chr(decode ^ key) for decode in decoded)

	return result

def repeating_key_xor(key,data):

	def xor(c1,c2):
		return '%0.2x' % (ord(c1) ^ ord(c2))

	k_s = ''.join([key for _ in range(0, int(len(data)/len(key)))] + [key[:len(data) - int(len(data)/len(key) * len(key))]])

	return ''.join(xor(x,y) for x, y in zip(k_s, data))

def edit_dist(str_1,str_2):

    edit_dist = 0

    for ed1, ed2 in zip(str_1,str_2):
        e1 = ord(ed1)
        e2 = ord(ed2)

        while e1 or e2:
            b1 = e1 & 1
            b2 = e2 & 1
            edit_dist += b1 ^ b2
            e1 >>= 1
            e2 >>= 1

    return edit_dist

def break_repeating_key_xor_dist_list(s):
    key_list = []
    dist_list = []
    KEYRANGE = 40

    for KEYSIZE in range(2,KEYRANGE+1):

        for x in range(0,2*KEYSIZE, KEYSIZE):
            key_list.append(''.join(s[x:x+KEYSIZE]))
       

        for i in range(0,len(key_list)-1):
            dist_list.append([KEYSIZE,(edit_dist(key_list[i],key_list[i+1]))/KEYSIZE])
        key_list = []
    
    return min(dist_list, key = lambda t:t[1])

def break_repeating_key_xor(s):

    block_text = []
    key = break_repeating_key_xor_dist_list(s)[0]

    trans_blocks = ['']*key
    
    for x in range(0,(len(s)//key),key):
        block_text.append(s[x:x+key])

    for block in block_text:
        for y in range(0,len(block)):
            trans_blocks[y] += ''.join(block[y])

    for blocks in trans_blocks:
        print(xor_cipher_break(blocks))




    







	





