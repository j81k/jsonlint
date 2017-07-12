import json
 
def dict_raise_on_duplicates(ordered_pairs):
    """Reject duplicate keys."""
    d = {}
    for k, v in ordered_pairs:
        if k in d:
           raise ValueError("Duplicate key is found: %r" % (k,))
        else:
           d[k] = v

    return d
 
def main():
    with open("input.json") as f:
    	try:
        	d = json.load(f, object_pairs_hook=dict_raise_on_duplicates)
        except ValueError as e:
				#pass
				text = str(e) #.pretty_description().replace('\n', '')
				#text = 'dsds'
				print('Error:::: ',text)	
 
    #print(d)

if __name__ == '__main__':
	main()    