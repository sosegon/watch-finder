class FinderView extends React.Component {
	constructor(props) {
		super(props)
		this.setup();
	}
	setup() {
		let w = 22;
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
			})
			.catch(function(err) {
				console.log("An error occured! " + err);
			});
	}
	processVideo() {
		let videoElem = this.refs.videoRef;
		let height = videoElem.height;
		let width = videoElem.width;
		let canvasInput = this.refs.canvasInRef;
		let context = canvasInput.getContext("2d");
		let canvasOutput = this.refs.canvasOutRef
		let src = new cv.Mat(height, width, cv.CV_8UC4);
		let dst = new cv.Mat(height, width, cv.CV_8UC1);
		let cap = new cv.VideoCapture(videoElem);

		const FPS = 30;

		let loop = function() {
			let begin = Date.now();
			cap.read(src);
			cv.cvtColor(src, dst, cv.COLOR_RGBA2GRAY);
			cv.imshow(canvasOutput, dst);
			// schedule next one.
			let delay = 100/FPS - (Date.now() - begin);
			setTimeout(loop, delay);
		}
		setTimeout(loop, 0);
	}
	render() {
		return(
			<div>
				<video ref="videoRef" height="240" width="320"></video>
				<canvas ref="canvasInRef" height="240" width="320"></canvas>
				<canvas ref="canvasOutRef" height="240" width="320"></canvas>
				<span onClick={this.startCamera.bind(this)}>Camera</span>
			</div>
		);
	}
}

let FinderViewRendered = ReactDOM.render(<FinderView />, document.getElementById('boardDiv'));