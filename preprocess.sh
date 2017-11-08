

: <<'END'

mkdir -p FB237-25
python remove_hub_node.py 25 FB237-25 

mkdir -p FB237-50
python remove_hub_node.py 50 FB237-50 

mkdir -p FB237-100
python remove_hub_node.py 100 FB237-100 

mkdir -p FB237-200
python remove_hub_node.py 200 FB237-200 

mkdir -p FB237-400
python remove_hub_node.py 400 FB237-400 

END

python test_graph_connection.py FB237-25 10 
python test_graph_connection.py FB237-50 8 
python test_graph_connection.py FB237-100 6 
python test_graph_connection.py FB237-200 4 
python test_graph_connection.py FB237-400 4 

