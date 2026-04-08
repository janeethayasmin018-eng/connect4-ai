import streamlit as st
import numpy as np
import random
import math
import copy

ROW_COUNT = 6
COL_COUNT = 7

# ---------- INIT ---------- #
if "board" not in st.session_state:
    st.session_state.board = np.zeros((ROW_COUNT, COL_COUNT))
    st.session_state.game_over = False

# ---------- FUNCTIONS ---------- #

def drop_piece(board, col, piece):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            board[r][col] = piece
            break

def is_valid(board, col):
    return board[ROW_COUNT - 1][col] == 0

def get_valid_moves(board):
    return [c for c in range(COL_COUNT) if is_valid(board, c)]

def win(board, piece):
    for c in range(COL_COUNT - 3):
        for r in range(ROW_COUNT):
            if all(board[r][c+i] == piece for i in range(4)):
                return True
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT - 3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True
    for c in range(COL_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True
    for c in range(COL_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True
    return False

# ---------- SIMPLE AI (FAST for mobile) ---------- #
def ai_move(board):
    moves = get_valid_moves(board)
    return random.choice(moves)

# ---------- UI ---------- #

st.title("🎮 Connect Four (AI Version)")

# Buttons
cols = st.columns(COL_COUNT)
for i in range(COL_COUNT):
    if cols[i].button(f"⬇️ {i}") and not st.session_state.game_over:
        if is_valid(st.session_state.board, i):
            drop_piece(st.session_state.board, i, 1)

            if win(st.session_state.board, 1):
                st.success("🎉 You Win!")
                st.session_state.game_over = True

            # AI turn
            if not st.session_state.game_over:
                ai_col = ai_move(st.session_state.board)
                drop_piece(st.session_state.board, ai_col, 2)

                if win(st.session_state.board, 2):
                    st.error("🤖 AI Wins!")
                    st.session_state.game_over = True

# Display board
board = np.flip(st.session_state.board, 0)

for row in board:
    line = ""
    for cell in row:
        if cell == 0:
            line += "⚪ "
        elif cell == 1:
            line += "🔴 "
        else:
            line += "🟡 "
    st.write(line)

# Reset button
if st.button("🔄 Restart Game"):
    st.session_state.board = np.zeros((ROW_COUNT, COL_COUNT))
    st.session_state.game_over = False
