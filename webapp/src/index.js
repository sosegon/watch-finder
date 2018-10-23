class FinderView extends React.Component {
	constructor(props) {
		super(props)
		this.setup();
	}
	setup() {
		// The step indicates the state of the GUI when interacting
		// with the user: 0 = idle, 1 = streaming, 2 = file, 3 = processing
		this.state = {step: 0};
	}
	shoot() {
		let videoElem = this.refs.videoRef;
		let height = videoElem.height;
		let width = videoElem.width;

		// OpenCV elements
		let srcMat = new cv.Mat(height, width, cv.CV_8UC4);
		let cap = new cv.VideoCapture(videoElem);
		cap.read(srcMat);

		// This is the canvas where the video captured by the camera will be displayed
		let canvasOutput = this.refs.canvasOutRef;
		let contextOutput = canvasOutput.getContext("2d");

		this.stopCamera();
		this.streaming = false;

		detector.detect(srcMat);
		let detections = detector.detections;
		if(detections.size() > 0) {
			let watchMat = detector.extract(srcMat)[0];
			let detection = detections.get(0);
			let final = utils.highlightBox(srcMat, detection);
			detector.drawDetections(final, canvasOutput, 1);
			this.setState({step: 3});
			this.search(watchMat);
		} else {
			this.setState({step: 0});
		}
	}
	search(watchMat) {
		// TODO: Implement the search
		let self = this;
		setTimeout(() => {
			self.setState({step: 0});
		}, 500);
	}
	startCamera() {
		let videoElem = this.refs.videoRef;
		let self = this;
		navigator.mediaDevices
			.getUserMedia({ video: true, audio: false })
			.then(function(stream) {
				videoElem.srcObject = stream;
				videoElem.play();
				self.stream = stream;
				self.streaming = true;
				self.processVideo();
				self.setState({step: 1});
			})
			.catch(function(err) {
				console.log("An error occured! " + err);
				self.state({step: 0});
			});
	}
	stopCamera() {
		let videoElem = this.refs.videoRef;
		videoElem.pause();
		videoElem.srcObject = null;

		if(this.stream) {
			this.stream.getVideoTracks()[0].stop();
		}
	}
	processVideo() {
		let videoElem = this.refs.videoRef;
		let height = videoElem.height;
		let width = videoElem.width;

		// Where we draw what is captured by the camera
		let canvasOutput = this.refs.canvasOutRef

		// OpenCV elements
		let srcMat = new cv.Mat(height, width, cv.CV_8UC4);
		let cap = new cv.VideoCapture(videoElem);

		let self = this;
		const FPS = 30;
		let loop = function() {

			if(!self.streaming) {
				srcMat.delete();
				return;
			}

			let begin = Date.now();
			cap.read(srcMat);

			detector.detect(srcMat);
			detector.drawDetections(srcMat, canvasOutput, 1);

			// schedule next one.
			let delay = 100/FPS - (Date.now() - begin);
			setTimeout(loop, delay);
		}
		setTimeout(loop, 0);
	}
	render() {
		let sourceButtonsClass = ["buttons-container"];
		let shootButtonsClass = ["buttons-container"];
		if(this.state.step === 0) {
			shootButtonsClass.push("buttons-container-disabled");
		} else if(this.state.step === 1) {
			sourceButtonsClass.push("buttons-container-disabled");
		} else if(this.state.step === 3) {
			shootButtonsClass.push("buttons-container-disabled");
			sourceButtonsClass.push("buttons-container-disabled");
		}
		sourceButtonsClass = sourceButtonsClass.join(" ");
		shootButtonsClass = shootButtonsClass.join(" ");
		return(
			<div>
				<video id="video-source" ref="videoRef" height="240" width="320"></video>
				<canvas className="canvas-image" ref="canvasOutRef" height="240" width="320"></canvas>
				<div className={sourceButtonsClass}>
					<span className="button" id="camera-button" onClick={this.startCamera.bind(this)}></span>
					<span className="button" id="folder-button"></span>
				</div>
				<div className={shootButtonsClass}>
					<span className="button" id="shooter-button" onClick={this.shoot.bind(this)}></span>
				</div>
			</div>
		);
	}
}

let utils = new Utils('errorMessage');
let detector = new Detector("cascade.xml", utils);

let FinderViewRendered = ReactDOM.render(<FinderView />, document.getElementById('boardDiv'));