# Music Visualizer

A professional React application for visualizing audio waveforms and beat patterns.

## Features

### 🎵 Core Features

#### Audio Upload Section
- Drag & drop + file selector (MP3, WAV support)
- Shows file name, size, and duration

#### Audio Waveform Visualization
- Real-time waveform display using wavesurfer.js
- Beat markers overlaid on the waveform

#### Beat Pattern Preview
- Toggle between waveform and beat pattern view
- Color-coded beats (strong vs weak beats)

#### Playback Controls
- Play / Pause / Stop / Seek
- Tempo slider (change BPM for testing)
- Volume control

### Additional Pages
- Home page with landing section
- Saved songs library
- FAQs section
- About page
- User profile

## Getting Started

### Prerequisites
- Node.js (v14 or higher)
- npm or yarn

### Installation

1. Clone the repository
```
git clone <repository-url>
```

2. Navigate to the project directory
```
cd music-visualizer
```

3. Install dependencies
```
npm install
```
or
```
yarn
```

### Running the Application

Start the development server:
```
npm run dev
```
or
```
yarn dev
```

The application will open automatically in your default browser at `http://localhost:3000`.

### Building for Production

To create a production build:
```
npm run build
```
or
```
yarn build
```

## Technologies Used

- React.js
- Vite
- Material UI
- wavesurfer.js
- React Router
- React Dropzone

## Project Structure

```
music-visualizer/
├── public/
├── src/
│   ├── assets/
│   ├── components/
│   │   └── Navbar.jsx
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── SavedSongs.jsx
│   │   ├── Faqs.jsx
│   │   ├── About.jsx
│   │   └── Profile.jsx
│   ├── App.jsx
│   ├── App.css
│   ├── main.jsx
│   ├── index.css
│   └── styles.css
├── index.html
├── package.json
├── vite.config.js
└── README.md
```
