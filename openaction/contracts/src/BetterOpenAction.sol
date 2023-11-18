// SPDX-License-Identifier: MIT

pragma solidity ^0.8.18;

import {HubRestricted} from 'lens/HubRestricted.sol';
import {Types} from 'lens/Types.sol';
import {IPublicationActionModule} from './interfaces/IPublicationActionModule.sol';
import {IBetter} from './interfaces/IBetter.sol';

contract BetterOpenAction is HubRestricted, IPublicationActionModule {
    mapping(uint256 profileId => mapping(uint256 pubId => string initMessage)) internal _initMessages;
    IBetter internal _better;
    
    constructor(address lensHubProxyContract, address betterContract) HubRestricted(lensHubProxyContract) {
        _better = IBetter(betterContract);
    }

    function initializePublicationAction(
        uint256 profileId,
        uint256 pubId,
        address /* transactionExecutor */,
        bytes calldata data
    ) external override onlyHub returns (bytes memory) {
        string memory initMessage = abi.decode(data, (string));

        _initMessages[profileId][pubId] = initMessage;

        return data;
    }

    function processPublicationAction(
        Types.ProcessActionParams calldata params
    ) external override onlyHub returns (bytes memory) {
        // string memory initMessage = _initMessages[params.publicationActedProfileId][params.publicationActedId];
        // (string memory actionMessage) = abi.decode(params.actionModuleData, (string));

        // bytes memory combinedMessage = abi.encodePacked(initMessage, " ", actionMessage);
        // _better.helloWorld(string(combinedMessage), params.transactionExecutor);

        // sends data to logic layer
        _better.filterData(params.actionModuleData, params.transactionExecutor);
        
    }
}