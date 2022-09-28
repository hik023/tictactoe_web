import React from "react";
import "./Board.css";
import {DOMAIN, WIN_STATUS, FIELD_SIZE} from "./Constants"


function Square(props) {
    return (
        <div className={props.className} onClick={props.onClick}>
            {props.value}
        </div>
    );
}


class Board extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            squares: Array(FIELD_SIZE * FIELD_SIZE).fill(null),
            win: Array(FIELD_SIZE * FIELD_SIZE).fill(false),
            isGameOver: false,
            xIsNext: true,
        };
    }


    componentDidMount() {
        fetch(DOMAIN + "/start_game", { 
            method: "GET",
            mode: "cors",
        })
    }


    handleClick(i) {
        const squares = this.state.squares.slice();
        if (!this.state.isGameOver && !squares[i]){
            squares[i] = this.state.xIsNext ? "X" : "O";
            this.setState({
                squares: squares,
                xIsNext: !this.state.xIsNext,
            });
            const jsonData = {
                cords: [parseInt(i / FIELD_SIZE), i % FIELD_SIZE],
                value: this.state.xIsNext ? 1 : 0
            }

            fetch(DOMAIN +"/set_value", { 
                method: "POST",
                mode: "cors",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(jsonData) 

            })
                .then(response => response.json())
                .then(data => {
                    if(data.status === WIN_STATUS){
                        const winners = this.state.win.slice();
                        data.data.win_line.forEach(el => {
                            winners[el[0] * FIELD_SIZE + el[1]] = true;
                        });
                        this.setState({
                            win: winners,
                            isGameOver: true
                        });
                    }
                });
        }
    }


    renderSquare(i) {
        return (
            <Square
                value={this.state.squares[i]}
                key={i}
                className={(this.state.squares[i] ? "square-filled" : "square") + " " + (this.state.win[i] ? "win" : "")}
                onClick={() => this.handleClick(i)}
            />
        );
    }


    render() {
        let status = "Next player: " + (this.state.xIsNext ? "X" : "O");
        if (this.state.isGameOver){
            status = "Player " + (this.state.xIsNext ? "O" : "X") +  " wins!!!";
        }
        const rows = [];
        for (let i = 0; i < FIELD_SIZE; i++){
            let row = [];
            for (let j = 0; j < FIELD_SIZE; j++){
                row.push(this.renderSquare(i * FIELD_SIZE + j));
            }
            rows.push(
                <div key={i} className="board-row">
                    {row}
                </div>
            )
        }

        return (
            <div>
                <div className="status">{status}</div>
                {rows}
                {this.state.isGameOver && 
                <button onClick={() => {window.location.reload();}} className="reload_btn">Play again</button>
                }
            </div>
        );
    }
}


export default Board;