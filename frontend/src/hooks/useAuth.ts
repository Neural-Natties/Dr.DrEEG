import { useEffect, useState } from 'react';

export const useSpotifyAuth = () => {
  const [token, setToken] = useState<string | null>(null);

  const login = async () => {
    // Get auth URL from backend
    const response = await fetch('/api/auth/login');
    const { url } = await response.json();
    // Redirect to Spotify login
    window.location.href = url;
  };

  useEffect(() => {
    // After redirect back, get token
    const code = new URLSearchParams(window.location.search).get('code');
    if (code) {
      fetch(`/api/auth/callback?code=${code}`)
        .then((res) => res.json())
        .then((data) => setToken(data.access_token));
    }
  }, []);

  return { token, login };
};
