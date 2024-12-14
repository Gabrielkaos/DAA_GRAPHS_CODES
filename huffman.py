
def build_tree(bin_tree):
    stack = []

    for node in reversed(bin_tree):
        if node[0] is None:
            right = stack.pop()
            left = stack.pop()
            stack.append((None, node[1],left,right))

        else:
            stack.append(node)

    return stack[0]

def build_dict(tree, prefix="", huffman=None):
    if huffman is None:huffman = {}

    if len(tree) == 2:
        huffman[tree[0]] = prefix
    else:
        build_dict(tree[2],prefix+'0',huffman)
        build_dict(tree[3],prefix+'1',huffman)

    return huffman


def encode(bin_tree, text):
    hier_tree = build_tree(bin_tree)
    huffman_dict = build_dict(hier_tree)
    text = text.lower().strip()

    encoded = ''.join(huffman_dict[char] for char in text if char in huffman_dict)

    return encoded

def decode(bin_tree, encoded):
    hier_tree = build_tree(bin_tree)
    decoded = []
    curr_tree = hier_tree

    for bit in encoded:
        if bit=="0":
            curr_tree = curr_tree[2]
        elif bit=="1":
            curr_tree = curr_tree[3]
        
        if len(curr_tree)==2:
            decoded.append(curr_tree[0])
            curr_tree = hier_tree
    return ''.join(decoded)
def huffman(text):
    
    freq_table = {}
    for line in text:
        for char in line.lower().strip():
            if char in freq_table:
                freq_table[char] += 1
            else:
                freq_table[char] = 1

    frequency = [[key, value] for key,value in freq_table.items()]
    frequency.sort(key=lambda i: i[1])
    
    # left smallest right biggest
    bin_tree = [frequency[0], frequency[1]]
    node = [None, bin_tree[0][1] + bin_tree[1][1]]
    bin_tree.insert(0,node)

    for i in frequency[2:]:
        if i[1] > bin_tree[0][1]:
            bin_tree.insert(1, i)
        else:
            bin_tree.insert(0, i)
        node = [None, bin_tree[0][1] + bin_tree[1][1]]
        bin_tree.insert(0,node)

    return bin_tree


file = 'file.txt'    
with open(file,'r') as f:
    text = f.readlines()

bin_tree = huffman(text)
hier_tree = build_tree(bin_tree)
huff_dict = build_dict(hier_tree)

text_to_encode = ''.join(text)

encoded = encode(bin_tree, text_to_encode)
decoded = decode(bin_tree,encoded)

print("Tree:")
print(hier_tree)
print()
print("Huffman dict:")
for i,code in huff_dict.items():
    print(f"{i}:{code}")
print()
print("Bin tree:")
print(bin_tree)
print()
print("Encoded:")
print(encoded)
print()
print("Decoded:")
print(decoded)