# Module 1 - Create a Blockchain
# ErayBD

# importing the libraries
import datetime # each block will have its own timestamp (created, mined...)
import hashlib  # hash the blocks
import json     # convert to blocks to readable format for postman

from flask import Flask, jsonify # flask: web app, jsonify: return messages to postman

# in SHA-256 encoding system, it only accept encoded strings. So, the hashes has to be string.

# part 1 - building a blockchain

class Blockchain:
    
    def __init__(self): # type of constructor on java
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
        
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,     # every block has each number by starting 1
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
        self.chain.append(block)    # the block that we just created, added to the chain
        return block    # we returned it to see on postman
    
    def get_previous_block(self):    # returns the last block of the chain
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):    # the rule-setter
        new_proof = 1
        check_proof = False
        
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest() # the rule we set
            
            # our condition is (new_proof**2 - previous_proof**2). if it is provided, it will be added to the chain.
            
            # hashlib - class
            # sha256 - encoding type
            # sha256's methods - a rule that we have set (new_proof**2 - previous_proof**2)
            # encode - regulates the sha256 encoding as it should be
            # hexdigest - turns the encoded value into a hexdigits which is 64 character long string
            
            if (hash_operation[:4] == '0000'):  # if hash_operation variable's first four digits are 0000
                check_proof = True   # then we got what we want
                
            else:
                new_proof += 1  # if it is not, then try the other proofs
            
        return new_proof   # we returned it to see on postman
        
    def hash(self, block):  # returns the cryptographic hash of the block
        encoded_block = json.dumps(block, sort_keys = True).encode()     # json.dumps - takes an object and makes it a string
        return hashlib.sha256(encoded_block).hexdigest()
    
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]   # we starting to control if it is valid from block number one
        block_index = 1
        
        while (block_index < len(chain)):
            block = chain[block_index] # we just initialize the block as current block
            
            if (block['previous_hash'] != self.hash(previous_block)):
                # this if statement checks that: if the previous hash of our current block...
                # is different than the hash of it's previous block
                
                # we're using self.hash here 'cause hash is a method of the class Blockchain,
                # not a seperate class. So, self means 'in this class'
                
                return False
            
            previous_proof = previous_block['proof']    # proof of our previous block
            proof = block['proof']  # proof of our current block
            
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            
            if (hash_operation[:4] != '0000'):
                return False
            
            previous_block = block  # previous_block updated to our current block for the loop
            block_index += 1  # block_index updated for the loop
            # end of while loop
            
        return True     # if everything went well (confirmed that the chain is valid) then we return True
                

# part 2 - mining our blockchain

# creating a web app
app = Flask(__name__)
    
# creating a blockchain
blockchain = Blockchain()   # a blockchain object from Blockchain class
    
# mining a new block
@app.route("/mine_block", methods=['GET'])
def mine_block():   # mining a block
    previous_block = blockchain.get_previous_block()    
    previous_proof = previous_block['proof']
    previous_hash = blockchain.hash(previous_block)
    
    proof = blockchain.proof_of_work(previous_proof)
    block = blockchain.create_block(proof, previous_hash)    # a new block mined with the all infos
    
    response = {'message': 'Congrulations, you just mined a block!',        # left side is dictionary of block
                'index': block['index'],                                    # right side is the info we got
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    # response is a dictionary
    
    return jsonify(response), 200 # 200 means OK on HTTP Status Codes

@app.route("/get_chain", methods=['GET'])   
def get_chain():    # write down the blockchain list with the all infos
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    
    return jsonify(response), 200

@app.route("/is_valid", methods=['GET'])
def is_valid():     # checking if the blockchain is valid
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    
    if (is_valid):
        response = {'message': 'All good. The Blockchain is valid.'}
        return jsonify(response), 200
    
    else:
        response = {'message': 'Something is wrong. The Blockchain is not valid.'}
        return jsonify(response), 406   # 406 means NOT ACCEPTABLE on HTTP Status Codes
        

# running the app
app.run(host = '0.0.0.0', port = 5000)
    
   










