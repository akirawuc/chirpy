// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import {IBetter} from "./interfaces/IBetter.sol";

contract Better is IBetter {
    uint betID;

    mapping (uint=>bool) activeBet;
    mapping (uint=>bool) closedBet;

    mapping (uint=>uint) numChoices;
    mapping (uint=>mapping (uint=>string)) choiceString;
    mapping (uint=>mapping (address=>uint)) chosen;
    mapping (uint=>mapping (address=>uint)) betAmount;
    mapping (uint=>uint) correctChoice;
    mapping (uint=>mapping(address=>bool)) participants;
    mapping (uint=>mapping(address=>bool)) judges;
    mapping (uint=>mapping(address=>bool)) betAdmin;
    mapping (uint=>bytes) betQuestions;

    struct BetDataParams {
        uint functionName;
        bytes params;
    }

    struct NewBetParams {
        bytes question;
        uint numChoices;
        string[] choiceString;
        address[] participants;
        address judge;
    }

    struct JoinBetParams {
        uint betID;
        uint choice;
        address joiner;
        uint amountBet;
        address currency;
    }

    struct AddJudgeParams {
        uint betID;
        address judge;
    }

    struct ResolveBetParams {
        uint betID;
        uint choice;
    }

    event Greet(string message, address actor);

    constructor() {
        betID = 0;
    }

    function filterData(bytes calldata data, address actor) external {
        BetDataParams memory method = abi.decode(data, (BetDataParams));
        if (method.functionName == 1) {
            return newBet(method.params, actor);
        }
        if (method.functionName == 2) {
            return joinBet(method.params);
        }
        if (method.functionName == 3) {
            return setJudge(method.params, actor);
        }
        if (method.functionName == 4) {
            return resolveBet(method.params, actor);
        }
    }

    
    function helloWorld(string memory message, address actor) external {
        emit Greet(string(abi.encodePacked("Hello, World! ", message)), actor);
    }

    function newBet(bytes memory data, address executor) public {
        NewBetParams memory params = abi.decode(data, (NewBetParams));
        require(params.numChoices >= 2);
        betID++;
        activeBet[betID] = true;
        numChoices[betID] = params.numChoices;
        for (uint i=0; i<params.numChoices; i++) {
            choiceString[betID][i] = params.choiceString[i];
        }
        betQuestions[betID] = params.question;
        if (params.judge != address(0)) {
            judges[betID][params.judge] = true;
        } else {
            judges[betID][executor] = true;
        }
        betAdmin[betID][executor] = true;
    }

    // lets user join the bet
    function joinBet(bytes memory data) public {
        JoinBetParams memory params = abi.decode(data, (JoinBetParams));
        require(activeBet[params.betID]);   // requires active bet
        // adds any joiner's monetary bets
        if (params.currency != address(0)){
            betAmount[params.betID][params.joiner] = betAmount[params.betID][params.joiner] + params.amountBet;
        }
        // sets joiner's choice
        chosen[params.betID][params.joiner] = params.choice;
        participants[params.betID][params.joiner] = true;
    }

    function setJudge(bytes memory data, address executor) public {
        AddJudgeParams memory params = abi.decode(data, (AddJudgeParams));
        require(betAdmin[params.betID][executor]);
        judges[params.betID][params.judge] = true;
    }

    function resolveBet(bytes memory data, address executor) public {
        ResolveBetParams memory params = abi.decode(data, (ResolveBetParams));
        require(judges[params.betID][executor]);
        correctChoice[params.betID] = params.choice;
        activeBet[params.betID] = false;
        closedBet[params.betID] = true;
    }
}