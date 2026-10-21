import streamlit as st
from data import regulars_p, positions
from squad import Squad
from assistant import ask_squad

st.set_page_config(page_title="FPL Squad Picker", page_icon="⚽")

st.title("⚽ FPL Squad Picker")
st.caption("Picks a legal 15-player squad from live FPL data, then lets you ask an AI assistant about it.")

# remember things between clicks
if "squad" not in st.session_state:
    st.session_state.squad = None
if "chat" not in st.session_state:
    st.session_state.chat = []

if st.button("Build my squad", type="primary"):
    squad = Squad()
    for p in regulars_p:
        if squad.can_add(p):
            squad.add(p)
    st.session_state.squad = squad
    st.session_state.chat = []

squad = st.session_state.squad

if squad:
    c1, c2 = st.columns(2)
    c1.metric("Squad cost", f"£{100 - squad.budget:.1f}m")
    c2.metric("Money left", f"£{squad.budget:.1f}m")

    for pos in positions.values():
        st.subheader(pos)
        rows = [
            {
                "Player": p["name"],
                "Club": p["team"],
                "Price (£m)": round(p["price"], 1),
                "Score": round(p["score"], 2),
                "Form": p["form"],
                "Points": p["points"],
            }
            for p in squad.picks
            if p["position"] == pos
        ]
        st.dataframe(rows, hide_index=True)

    st.divider()
    st.subheader("Ask about your squad")

    for msg in st.session_state.chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    question = st.chat_input("e.g. Who should I captain?")
    if question:
        st.session_state.chat.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = ask_squad(squad, question)
            st.markdown(answer)
        st.session_state.chat.append({"role": "assistant", "content": answer})
else:
    st.info("Click **Build my squad** to get started.")