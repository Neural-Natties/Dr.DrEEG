import React, { useState, useEffect } from 'react';

const defaultTrack = {
    name: "No track playing",
    album: {
        images: [
            { url: "https://via.placeholder.com/150" } // Placeholder image URL
        ]
    },
    artists: [
        { name: "Unknown artist" }
    ]
};

const track = {
    name: "",
    album: {
        images: [
            { url: "" }
        ]
    },
    artists: [
        { name: "" }
    ]
}

interface WebPlaybackProps {
    token: string;
    onPlayerReady: (deviceId: string) => void;
}

const WebPlayback: React.FC<WebPlaybackProps> = ({ token, onPlayerReady }) => {
    const [is_paused, setPaused] = useState(false);
    const [is_active, setActive] = useState(false);
    const [player, setPlayer] = useState<Spotify.Player | undefined>(undefined);
    const [current_track, setTrack] = useState(track);

    useEffect(() => {

        const script = document.createElement("script");
        script.src = "https://sdk.scdn.co/spotify-player.js";
        script.async = true;

        document.body.appendChild(script);

        window.onSpotifyWebPlaybackSDKReady = () => {
            const player = new window.Spotify.Player({
                name: 'Web Playback SDK 2',
                getOAuthToken: cb => { cb(token); },
                volume: 0.5
            });

            setPlayer(player);

            player.addListener('ready', ({ device_id }) => {
                fetch('https://api.spotify.com/v1/me/player', {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        device_ids: [device_id],
                        play: true
                    })    
                })
                .then(() => onPlayerReady(device_id))
            });

            player.addListener('not_ready', ({ device_id }) => {
                console.log('Device ID has gone offline', device_id);
                setActive(false);
            });

            player.addListener('player_state_changed', ( state => {
                if (!state) {
                    return;
                }

                setTrack(state.track_window.current_track);
                setPaused(state.paused);

                player.getCurrentState().then( state => { 
                    (!state)? setActive(false) : setActive(true) 
                });

            }));

            player.connect();

        };
    }, []);

        if (!is_active || !player || !current_track) { 
            return (
                <>
                    <div>
                        <div>
                            <b> Loading </b>
                        </div>
                    </div>
                </>)
        } else {
            return (
                <>
                    <div>
                        <div>
                            <div className="text-white">
                                <button className="btn-spotify" onClick={() => { player.previousTrack() }} >
                                    &lt;&lt;
                                </button>

                                <button className="btn-spotify" onClick={() => { player.togglePlay() }} >
                                    { is_paused ? "PLAY" : "PAUSE" }
                                </button>

                                <button className="btn-spotify" onClick={() => { player.nextTrack() }} >
                                    &gt;&gt;
                                </button>
                            </div>
                        </div>
                    </div>
                </>
            );
        }
    }

export default WebPlayback