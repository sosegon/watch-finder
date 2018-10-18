class FinderView extends React.Component {
	constructor(props) {
		super(props)
		this.setup();
	}
	setup() {
		// The step indicates the state of the GUI when interacting
		// with the user: 0 = idle, 1 = camera, 2 = file, 3 = processing
		this.state = {step: 0};
	}
	startCamera() {
		let videoElem = this.refs.videoRef;
		let self = this;
		navigator.mediaDevices
			.getUserMedia({ video: true, audio: false })
			.then(function(stream) {
				videoElem.srcObject = stream;
				videoElem.play();
				self.processVideo();
				self.state = {step: 1};
			})
			.catch(function(err) {
				console.log("An error occured! " + err);
			});
	}
	processVideo() {
		let videoElem = this.refs.videoRef;
		let height = videoElem.height;
		let width = videoElem.width;

		// This is the canvas where the video captured
		// by the camera will be displayed
		let canvasOutput = this.refs.canvasOutRef

		// The matrix elements where the image information
		// will be stored
		let src = new cv.Mat(height, width, cv.CV_8UC4);
		let gray = new cv.Mat();

		let cap = new cv.VideoCapture(videoElem);
		let objects = new cv.RectVector(); // where the detected objects will be stored
		let classifier = new cv.CascadeClassifier(); // the classifier for detection

		classifier.load(faceCascadeFile); // load pre-trained classifiers

		const FPS = 30;

		let loop = function() {
			let begin = Date.now();
			cap.read(src);

			// The detection is done using grayscale images
			cv.cvtColor(src, gray, cv.COLOR_RGBA2GRAY, 0);
			classifier.detectMultiScale(src, objects, 5.1, 6, 0);

			// Draw rectangles or every detection
			for (let i = 0; i < objects.size(); ++i) {
				let object = objects.get(i);
				let point1 = new cv.Point(object.x, object.y);
				let point2 = new cv.Point(object.x + object.width, object.y + object.height);
				cv.rectangle(src, point1, point2, [255, 0, 0, 255]);
			}
			cv.imshow(canvasOutput, src);

			// schedule next one.
			let delay = 100/FPS - (Date.now() - begin);
			setTimeout(loop, delay);
		}
		setTimeout(loop, 0);
	}
	render() {
		return(
			<div>
				<video id="video-source" ref="videoRef" height="240" width="320"></video>
				<canvas className="canvas-image" ref="canvasOutRef" height="240" width="320"></canvas>
				<div className="buttons-container">
					<span className="button" id="camera-button" onClick={this.startCamera.bind(this)}></span>
					<span className="button" id="folder-button"></span>
				</div>
			</div>
		);
	}
}

const faceCascadeFile = 'cascade.xml';
let utils = new Utils('errorMessage');
// utils.loadOpenCv(() => {
    utils.createFileFromUrl(faceCascadeFile, faceCascadeFile, () => {
        console.log("Cascade file downloaded");
    });
// });

let FinderViewRendered = ReactDOM.render(<FinderView />, document.getElementById('boardDiv'));