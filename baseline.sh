
#TransE
./Train_TransE -input ../../reinforce-walk/FB237-25/ -en 14541 -rn 237 -size 100 -margin 2 -method 0
./Test_TransE unif ../../reinforce-walk/FB237-25/ 14541 237
 
./Train_TransE -input ../../reinforce-walk/FB237-50/ -en 14541 -rn 237 -size 100 -margin 2 -method 0
./Test_TransE unif ../../reinforce-walk/FB237-50/ 14541 237

./Train_TransE -input ../../reinforce-walk/FB237-100/ -en 14541 -rn 237 -size 100 -margin 2 -method 0
./Test_TransE unif ../../reinforce-walk/FB237-100/ 14541 237

./Train_TransE -input ../../reinforce-walk/FB237-200/ -en 14541 -rn 237 -size 100 -margin 2 -method 0
./Test_TransE unif ../../reinforce-walk/FB237-200/ 14541 237

./Train_TransE -input ../../reinforce-walk/FB237-400/ -en 14541 -rn 237 -size 100 -margin 2 -method 0
./Test_TransE unif ../../reinforce-walk/FB237-400/ 14541 237


#TransR
./Train_TransR -input ../../reinforce-walk/FB237-25/ -init ../TransE/FB237-25/ -en 14541 -rn 237 -size 100 -margin 2 -method 0
./Test_TransR unif ../../reinforce-walk/FB237-25/ 14541 237

./Train_TransR -input ../../reinforce-walk/FB237-50/ -init ../TransE/FB237-50/ -en 14541 -rn 237 -size 100 -margin 2 -method 0
./Test_TransR unif ../../reinforce-walk/FB237-50/ 14541 237

./Train_TransR -input ../../reinforce-walk/FB237-100/ -init ../TransE/FB237-100/ -en 14541 -rn 237 -size 100 -margin 2 -method 0
./Test_TransR unif ../../reinforce-walk/FB237-100/ 14541 237
