import pickle
my_object = some_complicated_thing  #Like a list or dict or something, something that'd be annoying to figure out how to save to a file
savefile = open('myfilename.pkl', 'wb')  #If you're curious, 'wb' stands for 'write binary', as opposed to text
pickle.dump(my_object, savefile)  #Complicated thing is now saved

# Then, maybe in some other part of your code / in another file:

savefile = open('myfilename.pkl', 'rb')  #Read binary
my_object = pickle.load(savefile)  #This restores your object to whatever it was before you pickled it