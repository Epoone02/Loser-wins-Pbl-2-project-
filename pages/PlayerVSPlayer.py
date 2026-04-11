import streamlit as st
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import Bid_tree 

@st.cache_resource
def get_global_memory():
    return {
        "bids": [],
        "bank": {},
        "base_cost": 1.0,
        "alpha": 49.0
    }

memory = get_global_memory()

st.sidebar.title(" Game Settings")
current_view = st.sidebar.radio("Switch View:", ["Player View", " Host View"])



if current_view == "Player View":
    st.title("Place your bid! ")
    base_cost= memory['base_cost']
    alpha = memory['alpha']
    
    player_name = st.text_input("Enter your Username:")
    
    if player_name:
        if player_name not in memory["bank"]:
            memory['bank'][player_name] = 100.0
            
        current_balance = memory['bank'][player_name]
        st.info(f" **Current Balance:** ${current_balance:.2f}")
        
        if current_balance > 0:
            max_bid = int(current_balance)
            
            if max_bid > 0:
                proposed_price = st.slider("Select your Bid Price", min_value=0, max_value=max_bid, value=0, step=1)
            else:
                proposed_price = 0
                st.warning("Your balance is too low to bid higher than 0.")
            
            # Risk premium calculation
            bid_cost = base_cost + (alpha / (proposed_price + 1))
            st.write(f" **Cost of this ticket:** ${bid_cost:.2f}")
            
            if bid_cost > current_balance:
                st.error(" You don't have enough money to pay the ticket cost!")
            else:
                if st.button("Submit Bid"):
                    memory['bank'][player_name] -= bid_cost
                    memory['bids'].append({
                        "name": player_name, 
                        "price": proposed_price, 
                        "cost": bid_cost
                    })
                    st.success(f"Bid of ${proposed_price} placed!")
        else:
            st.error("You are bankrupt! ")


elif current_view == " Host View":
    st.title("Host Dashboard ")
    st.write(f"**Total bids received:** {len(memory['bids'])}")

    with st.expander("⚙️ Configure Game Rules", expanded=True):
        memory['base_cost'] = st.number_input("Base Cost", min_value=0.0, value=memory['base_cost'], step=0.5)
        memory['alpha'] = st.number_input("Alpha Parameter (a)", min_value=0.0, value= memory['alpha'], step=1.0)
    
    st.divider()

    if len(memory['bids']) > 0:
        if st.button(" Resolve Round", type="primary"):            
           
            tree = Bid_tree()
            total_seller_revenue = 0
            
           
            for bid in memory['bids']:
                tree.insert(bid["name"], bid["price"])
                total_seller_revenue += bid["cost"]
            
            st.success("Tree generated!")
            
            sorted_nodes = tree.get_inorder_nodes()
            winner = None
            
            st.subheader("Bid Results (Ascending Order)")
            for node in sorted_nodes:
                num_players = len(node.names)
                status = "UNIQUE" if num_players == 1 else " DUPLICATE"
                st.write(f"- Price **{node.bid}** proposed by {num_players} player(s) ({', '.join(node.names)}) -> {status}")
                
                
                if num_players == 1 and winner is None:
                    winner = {"price": node.bid, "player": node.names[0]}
            
            st.divider()
            
            st.subheader(" Final Result")
            if winner:
                st.balloons()
                st.write(f"The winner is **{winner['player']}** with the unique price of **{winner['price']}**! ")
            else:
                st.warning("No winner! Every price was proposed at least twice.")
                
            st.metric(label="Seller Revenue", value=f"${total_seller_revenue:.2f}")
            
        if st.button("Clear current round bids"):
            memory['bids'] = []
            st.rerun()
    else:
        st.info("Waiting for players...")