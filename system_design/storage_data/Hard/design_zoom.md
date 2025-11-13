# Design Zoom (Video Conferencing Platform)

**Difficulty:** Hard

## 1. Problem Statement

Design a real-time video conferencing platform like Zoom that supports high-quality video/audio calls, screen sharing, recording, and chat for meetings with hundreds of participants. The system must provide low-latency communication globally, handle network conditions gracefully, and scale to millions of concurrent meetings.

**Key Challenges:**
- Real-time audio/video with < 150ms latency
- Support 100-1000 participants per meeting
- Global distribution (low latency worldwide)
- Network adaptability (poor connections)
- Recording and storage
- Screen sharing with high quality

## 2. Requirements

### Functional Requirements
1. **Video/Audio Calling**:
   - One-on-one calls
   - Group meetings (up to 1000 participants)
   - Gallery view and speaker view
2. **Screen Sharing**: Share entire screen or specific window
3. **Chat**: In-meeting text chat with file sharing
4. **Recording**: Record meetings (cloud/local)
5. **Virtual Backgrounds**: AI-powered background replacement
6. **Breakout Rooms**: Split meeting into sub-rooms
7. **Waiting Room**: Host controls participant entry
8. **Reactions**: Emoji reactions, hand raising

### Non-Functional Requirements
1. **Latency**: < 150ms end-to-end for audio/video
2. **Quality**:
   - Video: 720p/1080p (adaptive)
   - Audio: 48kHz, 16-bit
3. **Scalability**:
   - 300 million daily meeting participants
   - 30 million concurrent users
   - Meetings with 1000 participants
4. **Availability**: 99.9% uptime
5. **Network Adaptability**:
   - Work on 3G/4G/5G/WiFi
   - Handle packet loss, jitter
6. **Security**: End-to-end encryption (E2EE)

## 3. Storage Estimation

### Assumptions
- **Daily Meetings**: 30 million
- **Average Meeting Duration**: 45 minutes
- **Average Participants**: 5 per meeting
- **Recording Rate**: 30% of meetings
- **Video Bitrate**: 2 Mbps average
- **Audio Bitrate**: 64 kbps

### Calculations

**Concurrent Meetings:**
```
30M daily meetings × 45 min avg
Average concurrency: 30M × 45/1440 = 937,500 concurrent meetings
Peak (3x): 2.8M concurrent meetings
```

**Bandwidth (Real-time):**
```
Per participant sending:
- Video: 2 Mbps
- Audio: 64 kbps
- Total: ~2.1 Mbps

Per participant receiving (in 5-person meeting):
- 4 video streams × 2 Mbps = 8 Mbps
- 4 audio streams × 64 kbps = 256 kbps
- Total: ~8.3 Mbps

Global bandwidth (30M concurrent users):
30M × 2.1 Mbps = 63 Tbps upload
30M × 8.3 Mbps = 249 Tbps download
Total: 312 Tbps
```

**Recording Storage:**
```
30M meetings/day × 30% recorded = 9M recordings/day

Per recording:
- Duration: 45 min avg
- Video bitrate: 2 Mbps
- Audio bitrate: 64 kbps
- Size: (2 + 0.064) Mbps × 45 × 60 = 5.6 GB

Daily storage: 9M × 5.6 GB = 50.4 PB/day
Monthly: 50.4 × 30 = 1,512 PB = 1.5 Exabytes (EB)
```

**Metadata Storage:**
```
Per meeting: 10 KB (participants, duration, settings)
30M meetings × 10 KB = 300 GB/day
```

## 4. High-Level Architecture

```
┌────────────────────────────────────────────────────────┐
│                 Client Layer                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │Desktop   │  │ Mobile   │  │  Web     │           │
│  │ Client   │  │   App    │  │ (WebRTC) │           │
│  └──────────┘  └──────────┘  └──────────┘           │
└────────────────────────────────────────────────────────┘
                       │
                       │ WebSocket / UDP (SRTP)
                       ▼
            ┌──────────────────────┐
            │   Global CDN /       │
            │   Anycast Network    │
            └──────────┬───────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Edge PoP   │ │   Edge PoP   │ │   Edge PoP   │
│   (US-East)  │ │   (EU-West)  │ │  (Asia-Pac)  │
│              │ │              │ │              │
│┌────────────┐│ │┌────────────┐│ │┌────────────┐│
││   Media    ││ ││   Media    ││ ││   Media    ││
││   Server   ││ ││   Server   ││ ││   Server   ││
│└────────────┘│ │└────────────┘│ │└────────────┘│
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       └────────────────┼────────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
        ▼                               ▼
┌─────────────────┐         ┌─────────────────────┐
│  Control Plane  │         │   Data Plane        │
│                 │         │                     │
│┌───────────────┐│         │┌──────────────────┐ │
││API Servers    ││         ││ SFU (Selective   │ │
││(REST/WS)      ││         ││  Forwarding Unit)│ │
│└───────────────┘│         │└──────────────────┘ │
│┌───────────────┐│         │┌──────────────────┐ │
││Signaling      ││         ││ MCU (Multipoint  │ │
││Service (ICE)  ││         ││  Control Unit)   │ │
│└───────────────┘│         │└──────────────────┘ │
│┌───────────────┐│         │┌──────────────────┐ │
││Meeting Service││         ││ Recording Server │ │
│└───────────────┘│         │└──────────────────┘ │
└────────┬────────┘         └──────────┬──────────┘
         │                             │
    ┌────┴─────┬──────────────────────┘
    │          │
    ▼          ▼
┌─────────┐  ┌────────────┐
│Metadata │  │ Recording  │
│   DB    │  │  Storage   │
│(Spanner)│  │  (GCS/S3)  │
└─────────┘  └────────────┘
```

### Key Components

1. **Edge PoPs**: Geographically distributed (150+ locations)
2. **Media Server (SFU)**: Forwards media streams
3. **Signaling Service**: WebRTC handshake, ICE
4. **API Servers**: REST APIs, WebSocket
5. **Meeting Service**: Meeting lifecycle management
6. **Recording Server**: Record and store meetings
7. **MCU**: Mix/transcode for large meetings
8. **Metadata DB**: Meeting data, participants
9. **Recording Storage**: GCS/S3 for recordings

## 5. API Design

### Create Meeting
```http
POST /api/v1/meetings
Authorization: Bearer {token}

Request:
{
  "topic": "Weekly Standup",
  "type": "scheduled", // instant, scheduled, recurring
  "start_time": "2025-11-12T10:00:00Z",
  "duration": 60, // minutes
  "settings": {
    "host_video": true,
    "participant_video": true,
    "waiting_room": true,
    "recording": "cloud",
    "max_participants": 100
  }
}

Response (201 Created):
{
  "meeting_id": "meeting_abc123",
  "meeting_number": "123-456-789",
  "topic": "Weekly Standup",
  "start_url": "https://zoom.us/s/abc123?token=xyz",
  "join_url": "https://zoom.us/j/123456789",
  "password": "p@ssw0rd",
  "created_at": "2025-11-12T09:00:00Z"
}
```

### Join Meeting
```http
POST /api/v1/meetings/{meeting_id}/join
Authorization: Bearer {token}

Request:
{
  "display_name": "John Doe",
  "video_enabled": true,
  "audio_enabled": true,
  "device_info": {
    "os": "Windows 10",
    "browser": "Chrome 95"
  }
}

Response (200 OK):
{
  "participant_id": "part_xyz",
  "session_token": "session_token_abc",
  "media_server": "media.us-east-1.zoom.com",
  "signaling_server": "signal.us-east-1.zoom.com",
  "turn_servers": [
    {
      "urls": "turn:turn1.zoom.com:3478",
      "username": "user123",
      "credential": "cred456"
    }
  ],
  "ice_servers": [...]
}
```

### WebRTC Signaling
```javascript
// Client-side WebRTC setup
const pc = new RTCPeerConnection({
  iceServers: response.ice_servers
});

// Add local media tracks
navigator.mediaDevices.getUserMedia({video: true, audio: true})
  .then(stream => {
    stream.getTracks().forEach(track => {
      pc.addTrack(track, stream);
    });
  });

// Create offer
const offer = await pc.createOffer();
await pc.setLocalDescription(offer);

// Send offer to signaling server
ws.send(JSON.stringify({
  type: 'offer',
  sdp: offer.sdp,
  participant_id: participant_id
}));

// Receive answer
ws.onmessage = async (event) => {
  const message = JSON.parse(event.data);
  
  if (message.type === 'answer') {
    await pc.setRemoteDescription({
      type: 'answer',
      sdp: message.sdp
    });
  }
  
  if (message.type === 'ice-candidate') {
    await pc.addIceCandidate(message.candidate);
  }
};
```

## 6. Media Architecture

### SFU (Selective Forwarding Unit)

**Why SFU over Mesh or MCU?**

**Mesh (P2P):**
- ❌ Doesn't scale (n*(n-1)/2 connections)
- ❌ High client bandwidth
- ✅ Lowest latency

**MCU (Multipoint Control Unit):**
- ❌ High server CPU (encoding/decoding)
- ❌ Fixed layout
- ✅ Low client bandwidth

**SFU (Selective Forwarding Unit):**
- ✅ Scales to 100s of participants
- ✅ Adaptive layouts
- ✅ Low server CPU (no transcoding)
- ✅ Moderate client bandwidth

**SFU Implementation:**
```python
class SFU:
    def __init__(self):
        self.participants = {}  # participant_id → connection
        self.streams = {}  # stream_id → media stream
    
    def add_participant(self, participant_id, connection):
        self.participants[participant_id] = connection
        
        # Send existing streams to new participant
        for stream_id, stream in self.streams.items():
            if stream.owner != participant_id:
                connection.send_stream(stream)
    
    def receive_media(self, participant_id, stream):
        # Store stream
        stream_id = f"{participant_id}:{stream.track_id}"
        self.streams[stream_id] = stream
        
        # Forward to all other participants
        for pid, connection in self.participants.items():
            if pid != participant_id:
                connection.send_stream(stream)
    
    def remove_participant(self, participant_id):
        # Remove participant's streams
        for stream_id in list(self.streams.keys()):
            if stream_id.startswith(participant_id):
                del self.streams[stream_id]
        
        # Notify other participants
        for pid, connection in self.participants.items():
            if pid != participant_id:
                connection.notify_participant_left(participant_id)
        
        del self.participants[participant_id]
```

### Simulcast for Adaptive Quality

**Problem:** Participants have different bandwidth capabilities

**Solution:** Send multiple quality versions, SFU selects best for each receiver

```javascript
// Client sends 3 layers
const sender = pc.addTrack(videoTrack, stream);
await sender.setParameters({
  encodings: [
    {rid: 'high', maxBitrate: 2500000, scaleResolutionDownBy: 1},  // 1080p
    {rid: 'medium', maxBitrate: 1000000, scaleResolutionDownBy: 2}, // 540p
    {rid: 'low', maxBitrate: 300000, scaleResolutionDownBy: 4}      // 270p
  ]
});
```

**SFU Layer Selection:**
```python
def select_layer(self, receiver_bandwidth, cpu_capability):
    # Select appropriate layer based on receiver's bandwidth
    if receiver_bandwidth > 2000000 and cpu_capability > 0.7:
        return 'high'  # 1080p
    elif receiver_bandwidth > 800000:
        return 'medium'  # 540p
    else:
        return 'low'  # 270p
```

### Network Adaptation

**Bandwidth Estimation:**
```python
class BandwidthEstimator:
    def __init__(self):
        self.send_times = []
        self.ack_times = []
    
    def estimate_bandwidth(self):
        # Calculate based on packet send/ack times
        if len(self.ack_times) < 10:
            return 1000000  # 1 Mbps default
        
        # Recent 10 packets
        recent_sends = self.send_times[-10:]
        recent_acks = self.ack_times[-10:]
        
        # RTT calculation
        rtts = [ack - send for send, ack in zip(recent_sends, recent_acks)]
        avg_rtt = sum(rtts) / len(rtts)
        
        # Bandwidth = packet_size / RTT
        packet_size = 1500  # bytes
        bandwidth = (packet_size * 8) / avg_rtt  # bits per second
        
        return bandwidth
    
    def adapt_quality(self, bandwidth):
        if bandwidth < 500000:  # 500 kbps
            return {'video': False, 'audio': True}  # Audio only
        elif bandwidth < 1000000:  # 1 Mbps
            return {'video': '360p', 'audio': True}
        elif bandwidth < 2000000:  # 2 Mbps
            return {'video': '720p', 'audio': True}
        else:
            return {'video': '1080p', 'audio': True}
```

## 7. Scalability for Large Meetings

### SFU Cascade for 1000+ Participants

**Problem:** Single SFU can't handle 1000 participants

**Solution:** Hierarchical SFU cascade

```
                    ┌─────────┐
                    │ Root SFU│
                    └────┬────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
     ┌────────┐     ┌────────┐     ┌────────┐
     │SFU-1   │     │SFU-2   │     │SFU-3   │
     └───┬────┘     └───┬────┘     └───┬────┘
         │              │              │
    ┌────┴───┐     ┌────┴───┐     ┌────┴───┐
    │        │     │        │     │        │
 Part 1-100  │  Part 101-  │  Part 201-  │
             │  200        │  300        │
         Part 101-200   Part 201-300   Part 301-400
```

**Implementation:**
```python
class SFUCascade:
    def __init__(self, max_participants_per_sfu=100):
        self.root_sfu = SFU(is_root=True)
        self.child_sfus = []
        self.max_per_sfu = max_participants_per_sfu
    
    def add_participant(self, participant):
        # Find SFU with capacity
        target_sfu = None
        for sfu in self.child_sfus:
            if sfu.participant_count() < self.max_per_sfu:
                target_sfu = sfu
                break
        
        # Create new child SFU if needed
        if not target_sfu:
            target_sfu = SFU(parent=self.root_sfu)
            self.child_sfus.append(target_sfu)
            self.root_sfu.add_child(target_sfu)
        
        # Add participant to selected SFU
        target_sfu.add_participant(participant)
```

### Gallery View Optimization

**Problem:** Rendering 100 video tiles is CPU-intensive

**Solution:** Active speaker detection + selective rendering

```javascript
class GalleryView:
  constructor(maxVisible = 25) {
    this.maxVisible = maxVisible;
    this.allParticipants = [];
    this.visibleParticipants = [];
    this.activeSpeaker = null;
  }
  
  updateVisibleParticipants() {
    // Priority:
    // 1. Active speaker (always visible)
    // 2. Recently active speakers
    // 3. Pinned participants
    // 4. Others (sorted by join time)
    
    let visible = [];
    
    // Always include active speaker
    if (this.activeSpeaker) {
      visible.push(this.activeSpeaker);
    }
    
    // Add recent speakers (within last 10 seconds)
    let recentSpeakers = this.getRecentSpeakers(10);
    visible = visible.concat(recentSpeakers.slice(0, 8));
    
    // Add pinned
    let pinned = this.getPinnedParticipants();
    visible = visible.concat(pinned.slice(0, 5));
    
    // Fill remaining with others
    let remaining = this.maxVisible - visible.length;
    let others = this.allParticipants.filter(p => !visible.includes(p));
    visible = visible.concat(others.slice(0, remaining));
    
    this.visibleParticipants = visible;
    this.render();
  }
  
  detectActiveSpeaker() {
    // Use audio levels to detect who's speaking
    let maxAudioLevel = 0;
    let speaker = null;
    
    for (let participant of this.allParticipants) {
      let audioLevel = this.getAudioLevel(participant);
      
      if (audioLevel > maxAudioLevel && audioLevel > 0.3) {
        maxAudioLevel = audioLevel;
        speaker = participant;
      }
    }
    
    if (speaker !== this.activeSpeaker) {
      this.activeSpeaker = speaker;
      this.updateVisibleParticipants();
    }
  }
}
```

## 8. Screen Sharing

### High-Quality Screen Share

**Requirements:**
- Higher resolution (1080p/4K)
- Lower frame rate acceptable (10-15 fps)
- Text must be readable

**Implementation:**
```javascript
async function shareScreen() {
  // Capture screen
  const stream = await navigator.mediaDevices.getDisplayMedia({
    video: {
      width: {ideal: 1920},
      height: {ideal: 1080},
      frameRate: {ideal: 15, max: 30},
      cursor: 'always'
    },
    audio: false
  });
  
  // Add to peer connection with separate encoding
  const videoTrack = stream.getVideoTracks()[0];
  const sender = pc.addTrack(videoTrack, stream);
  
  await sender.setParameters({
    encodings: [{
      maxBitrate: 3000000,  // 3 Mbps
      scaleResolutionDownBy: 1  // No downscaling
    }]
  });
  
  // Notify server this is screen share (not webcam)
  ws.send(JSON.stringify({
    type: 'screen_share_started',
    track_id: videoTrack.id
  }));
}
```

**Optimization: Content-Aware Encoding**
```python
def encode_screen_share(frame):
    # Detect content type
    content_type = detect_content_type(frame)
    
    if content_type == 'text':
        # Use lossless compression for text
        return encode_h264(frame, profile='high', crf=18)
    elif content_type == 'video':
        # Video within screen share (e.g., YouTube)
        return encode_h264(frame, profile='main', crf=23)
    else:
        # Mixed content
        return encode_h264(frame, profile='main', crf=20)
```

## 9. Recording

### Cloud Recording Architecture

```
Meeting in Progress
    ↓
Recording Server joins as participant
    ↓
Receives all audio/video streams
    ↓
Mix/Composite streams
    ↓
Encode to single video file (H.264)
    ↓
Upload to GCS/S3 in chunks
    ↓
Post-processing (optional)
    ├─→ Generate thumbnails
    ├─→ Speech-to-text (captions)
    └─→ Speaker identification
    ↓
Store metadata in database
    ↓
Notify host when ready
```

**Recording Server:**
```python
class RecordingServer:
    def __init__(self, meeting_id):
        self.meeting_id = meeting_id
        self.streams = {}
        self.output_file = f"/tmp/recording_{meeting_id}.mp4"
        self.encoder = FFmpegEncoder()
    
    def start_recording(self):
        # Join meeting as hidden participant
        self.join_meeting(self.meeting_id)
        
        # Start encoder
        self.encoder.start(output=self.output_file)
    
    def receive_stream(self, participant_id, stream):
        self.streams[participant_id] = stream
        
        # Mix audio
        mixed_audio = self.mix_audio_streams()
        
        # Composite video (grid layout)
        composite_video = self.composite_video_streams()
        
        # Encode frame
        self.encoder.encode_frame(composite_video, mixed_audio)
    
    def composite_video_streams(self):
        # Create grid layout
        grid = self.create_grid_layout(len(self.streams))
        
        composite = np.zeros((1080, 1920, 3), dtype=np.uint8)
        
        for i, (pid, stream) in enumerate(self.streams.items()):
            frame = stream.get_latest_frame()
            x, y, w, h = grid[i]
            composite[y:y+h, x:x+w] = cv2.resize(frame, (w, h))
        
        return composite
    
    def mix_audio_streams(self):
        # Mix all audio streams
        mixed = np.zeros(480)  # 10ms at 48kHz
        
        for pid, stream in self.streams.items():
            audio_samples = stream.get_audio_samples()
            mixed += audio_samples
        
        # Normalize
        mixed = mixed / len(self.streams)
        return mixed
    
    def stop_recording(self):
        # Finalize encoding
        self.encoder.finalize()
        
        # Upload to cloud storage
        recording_url = self.upload_to_gcs(self.output_file)
        
        # Save metadata
        db.insert({
            'meeting_id': self.meeting_id,
            'recording_url': recording_url,
            'duration': self.encoder.duration,
            'size': os.path.getsize(self.output_file),
            'created_at': now()
        })
        
        # Notify host
        notify_host(self.meeting_id, recording_url)
```

## 10. Latency Optimization

### Global Edge Network

**Anycast DNS:**
- Client resolves zoom.us
- DNS returns nearest PoP IP
- Client connects to nearest server

**Latency Targets:**
```
Client → Nearest PoP: < 20ms
PoP → PoP: < 50ms (for relay)
Total end-to-end: < 150ms
```

### TURN Server for NAT Traversal

```python
class TURNServer:
    def __init__(self):
        self.allocations = {}  # client → allocated port
    
    def allocate_port(self, client_id):
        # Allocate UDP port for client
        port = self.find_available_port()
        self.allocations[client_id] = port
        
        return {
            'turn_server': 'turn.zoom.com',
            'port': port,
            'username': client_id,
            'credential': generate_credential(client_id)
        }
    
    def relay_packet(self, from_client, to_client, packet):
        # Relay RTP packet between clients
        to_port = self.allocations[to_client]
        self.send_udp(to_port, packet)
```

### Forward Error Correction (FEC)

**Problem:** Packet loss causes audio/video glitches

**Solution:** Send redundant data

```python
class FECEncoder:
    def encode(self, packets, redundancy=0.2):
        # Add 20% redundant packets
        num_redundant = int(len(packets) * redundancy)
        
        # Generate parity packets using XOR
        parity_packets = []
        for i in range(num_redundant):
            parity = bytes([0] * len(packets[0]))
            
            for packet in packets:
                parity = bytes([a ^ b for a, b in zip(parity, packet)])
            
            parity_packets.append(parity)
        
        return packets + parity_packets
    
    def decode(self, received_packets, expected_count):
        # Recover lost packets using parity
        if len(received_packets) >= expected_count:
            return received_packets[:expected_count]
        
        # Use parity to recover
        # ... (Reed-Solomon decoding)
```

## 11. Security

### End-to-End Encryption (E2EE)

```python
class E2EEManager:
    def __init__(self, meeting_id):
        self.meeting_id = meeting_id
        self.participants = {}
        self.encryption_key = None
    
    def generate_meeting_key(self):
        # Host generates random encryption key
        self.encryption_key = os.urandom(32)  # AES-256
    
    def distribute_key(self, participant_id, public_key):
        # Encrypt meeting key with participant's public key
        encrypted_key = rsa_encrypt(self.encryption_key, public_key)
        
        # Send encrypted key to participant
        self.send_to_participant(participant_id, encrypted_key)
    
    def encrypt_media(self, media_packet):
        # Encrypt RTP packet
        cipher = AES.new(self.encryption_key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(media_packet)
        
        return cipher.nonce + tag + ciphertext
    
    def decrypt_media(self, encrypted_packet):
        # Extract nonce, tag, ciphertext
        nonce = encrypted_packet[:16]
        tag = encrypted_packet[16:32]
        ciphertext = encrypted_packet[32:]
        
        # Decrypt
        cipher = AES.new(self.encryption_key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        
        return plaintext
```

### Waiting Room

```python
def admit_participant(host_id, participant_id):
    # Verify host
    if not is_host(host_id):
        raise Unauthorized()
    
    # Move participant from waiting room to meeting
    participant = db.get_participant(participant_id)
    participant.status = 'admitted'
    db.update(participant)
    
    # Send admission notification
    ws.send_to(participant_id, {
        'type': 'admitted',
        'meeting_id': participant.meeting_id
    })
    
    # Join participant to SFU
    sfu.add_participant(participant_id)
```

## 12. Trade-offs

### SFU vs. MCU

**SFU:**
- ✅ Low server CPU
- ✅ Scales better
- ❌ Higher client bandwidth

**MCU:**
- ✅ Low client bandwidth
- ❌ High server CPU
- ❌ Fixed layouts

**Decision:** SFU for most meetings, MCU for very large webinars

### WebRTC vs. Custom Protocol

**WebRTC:**
- ✅ Browser support
- ✅ NAT traversal (STUN/TURN)
- ❌ Overhead

**Custom:**
- ✅ Optimized for Zoom
- ✅ Lower latency
- ❌ No browser support

**Decision:** WebRTC for web, custom for native apps

## 13. Follow-up Questions

1. **How do you handle participant who dominates the conversation?**
   - Active speaker detection
   - Rotate speaking time
   - Host controls (mute)

2. **How would you implement breakout rooms?**
   - Create sub-meetings
   - Reassign participants to different SFUs
   - Host can broadcast to all rooms

3. **How do you detect poor network conditions?**
   - Monitor RTT, packet loss, jitter
   - Adjust video quality automatically
   - Show "unstable connection" warning

4. **How would you implement virtual backgrounds?**
   - ML model (body segmentation)
   - Replace background pixels
   - Run on client (GPU)

5. **How do you handle recordings of large meetings?**
   - Multiple recording servers
   - Each records subset of participants
   - Post-processing stitches together

## Complexity Analysis

- **Time Complexity:**
  - Join meeting: O(1)
  - Send media: O(n) where n = participants
  - Receive media: O(1)

- **Space Complexity:**
  - Per meeting: O(n × m) where n = participants, m = media streams
  - Per participant: O(n) for receiving all streams

## References

- [WebRTC Specifications](https://webrtc.org/)
- [SFU Architecture](https://webrtcglossary.com/sfu/)
- [Zoom Architecture](https://blog.zoom.us/)
- [Real-time Communication at Scale](https://www.youtube.com/watch?v=fVD1aT11y54)
