// SPDX-License-Identifier: MIT

pragma solidity >=0.8.0;

interface IBetter {
    function filterData(bytes calldata data, address actor) external;
    function helloWorld(string memory message, address actor) external;
    // function newBet(bytes calldata message, address actor) external;
    // function joinBet(bytes calldata message, address actor) external;
    // function setJudge(bytes calldata message, address actor) external;
    // function resolveBet(bytes calldata message, address actor) external;
}