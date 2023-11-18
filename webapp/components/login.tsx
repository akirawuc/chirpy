//@ts-nocheck
import { LensClient, development } from '@lens-protocol/client';
import {useAccount} from 'wagmi';

import { useSignMessage } from 'wagmi'
import { recoverMessageAddress } from 'viem'
import React, { useEffect, useState } from 'react';


const LensAuthentication = () => {
  const { address } = useAccount();
  const [client, setClient] = useState(null);
  const [challenge, setChallenge] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [profileId, setProfileId] = useState(null);
  const [accessToken, setAccessToken] = useState(null);
    const { data: signMessageData, signMessage, isLoading, error } = useSignMessage();

  useEffect(() => {
    if (address) {
      const client = new LensClient({
        environment: development,
        headers: {
          origin: 'https://lens-scripts.example',
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        },
      });
      setClient(client);
      initializeLensAuthentication(client, address);
    }
  }, [address]);
    

  const initializeLensAuthentication = async (client, address) => {
    const managedProfiles = await client.wallet.profilesManaged({ for: address });
    if (managedProfiles.items.length === 0) {
      throw new Error(`You don't manage any profiles, create one first`);
    }

    const { id, text } = await client.authentication.generateChallenge({
      signedBy: address,
      for: managedProfiles.items[0].id,
    });
      console.log(text);

    setChallenge({ id, text });

  };

  const handleSignedMessage = async (signature) => {
    if (client && challenge) {
      await client.authentication.authenticate({ id: challenge.id, signature });

      const accessTokenResult = await client.authentication.getAccessToken();
      const accessToken = accessTokenResult.unwrap();

      const profileId = await client.authentication.getProfileId();

      setIsAuthenticated(await client.authentication.isAuthenticated());
      setProfileId(profileId);
      setAccessToken(accessToken);
    }
      console.log(isAuthenticated);
      return {profileId, accessToken};
  };

return (
  <div>
    {challenge && (
        <button onClick={() => {
            const signature = signMessage({ message: challenge.text });
            // console.log(profileId, accessToken);
        }}>
        Sign Challenge
      </button>
    )}
    {isAuthenticated && (
      <div>
        <p>Is LensClient authenticated? {isAuthenticated.toString()}</p>
        <p>Authenticated profileId: {profileId}</p>
        <p>Access token: {accessToken}</p>
      </div>
    )}
  </div>
);
};

export default LensAuthentication;
