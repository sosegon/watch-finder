import {downloadModel} from "./index_yolo";

require('../css/main.scss');
let {Utils} = require("./utils.js");
let {YoloDetector} = require("./detector.js");
let React = require('react');
let ReactDOM = require('react-dom');

let utils = new Utils('errorMessage');

class FinderView extends React.Component {
	constructor(props) {
		super(props)
		this.setup();
	}
	setup() {
		// The step indicates the state of the GUI when interacting
		// with the user: 0 = idle, 1 = streaming, 2 = file, 3 = processing
		this.state = {step: 0, message: ""};
	}
	async shoot() {
		let videoElem = this.refs.videoRef;
		let height = videoElem.height;
		let width = videoElem.width;
		let canvasOutput = this.refs.canvasOutRef;

		// OpenCV elements
		let srcMat = new cv.Mat(height, width, cv.CV_8UC4);
		let cap = new cv.VideoCapture(videoElem);
		cap.read(srcMat);

		await this.detectWatch(videoElem, srcMat, canvasOutput);

		this.stopCamera();
		this.streaming = false;
		this.clearRects();
	}
	async detectWatch(htmlElem, srcMat, canvasOutput) {
		let boxes = await yoloDetector.detectObjects(htmlElem);
		boxes = boxes.filter(box => {return box.className === "clock";});

		if(boxes.length > 0) {
			let watchMat = yoloDetector.extract(srcMat, boxes[0]);
			let rect = yoloDetector.boxToRect(boxes[0]);
			let highlighted = utils.highlightBox(srcMat, rect);
			yoloDetector.drawBox(highlighted, canvasOutput, boxes[0]);

			// detector.drawBoxes(srcMat, canvasOutput, boxes);
			// TODO: Implemented the search, extract the watch
			this.search(watchMat);
			this.setState({step: 3, message: "Searching!"});
		} else {
			this.setState({step: 0, message: "No watch detected!"});
		}

	}
	search(watchMat) {
		// TODO: Implement the search
		let canvasAux = this.refs.canvasAuxRef;
		canvasAux.width = watchMat.cols;
		canvasAux.height = watchMat.rows;

		let grayMat = new cv.Mat();
		cv.cvtColor(watchMat, grayMat, cv.COLOR_RGB2GRAY);

		cv.imshow(canvasAux, grayMat);
		let base64 = canvasAux.toDataURL("image/jpeg");
		base64 = base64.split(',')[1]; // remove header

		let form = new FormData();
		form.append("data", base64);

		fetch('/search' , {
			method: 'POST',
			body: form
		}).then((response) => {
			if (response.status >= 200 && response.status <= 302) {
            	return response;
          	} else {
            	var error = new Error(response.statusText);
            	error.response = response;
            	throw error;
          	}
		}).then((response) => {
			return response.text().then((text) => {
				console.log(text);
			})
		});

		let self = this;
		setTimeout(() => {
			self.setState({step: 0, message: ""});
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
				self.run();
				self.setState({step: 1, message: ""});
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
	async run() {
		let self = this;
		let videoElem = this.refs.videoRef;

		while(self.streaming) {
			let boxes = await yoloDetector.detectObjects(videoElem);
			self.clearRects();

			boxes
			.filter(box => {
				return box.className === "clock";
			})
			.forEach(box => {
				const {
					top, left, bottom, right, classProb, className
				} = box;

				self.drawRect(left, top, right-left, bottom-top);
			});
		}

		// clear any remaining rect, useful when shooting
		self.clearRects();
	}
	clearRects() {
		const rects = document.getElementsByClassName('rect');
		  while(rects[0]) {
			rects[0].parentNode.removeChild(rects[0]);
		  }
	}
	drawRect(x, y, w, h, color = 'red') {
		let videoWrapperElem = this.refs.videoWrapperRef;
		const rect = document.createElement('div');
		rect.classList.add('rect');

		let xx = x + 69; // correction due to width of video
		rect.style.cssText = 'top:' + y + 'px; left:' + xx + 'px; width:' + w + 'px; height:' + h + 'px; border-color:' + color;

		videoWrapperElem.appendChild(rect);
	}
	loadImage(event) {
		if (event.target.files && event.target.files[0]) {
			let canvasOutput = this.refs.canvasOutRef;
			let height = canvasOutput.height;
			let width = canvasOutput.width;
			let ctx = canvasOutput.getContext('2d');

			let self = this;

			let reader = new FileReader();
			reader.onload = (e) => {
				let img = new Image();
				img.crossOrigin = 'anonymous';
				img.onload = function() {
					ctx.drawImage(img, 0, 0, width, height);
					self.setState({step: 2, message: ""});
					self.detectWatch(canvasOutput, new cv.imread(canvasOutput), canvasOutput);
				};
				img.src = e.target.result;
			};
			reader.readAsDataURL(event.target.files[0]);
		}
	}
	bindToInput() {
		let inputImg = this.refs.inputImgRef;
		inputImg.click();
	}
	render() {
		let sourceButtonsClass = ["buttons-container"];
		let shootButtonsClass = ["buttons-container"];
		let videoSourceClass = [];
		let canvasClass = [];
		if(this.state.step === 0) {
			shootButtonsClass.push("buttons-container-disabled");
			videoSourceClass.push("block-hid");
		} else if(this.state.step === 1) {
			sourceButtonsClass.push("buttons-container-disabled");
			canvasClass.push("block-hid");
		} else if(this.state.step === 2) {
			videoSourceClass.push("block-hid");
		} else if(this.state.step === 3) {
			shootButtonsClass.push("buttons-container-disabled");
			sourceButtonsClass.push("buttons-container-disabled");
			videoSourceClass.push("block-hid");
		}
		sourceButtonsClass = sourceButtonsClass.join(" ");
		shootButtonsClass = shootButtonsClass.join(" ");
		videoSourceClass = videoSourceClass.join(" ");
		canvasClass = canvasClass.join(" ");


		let message = this.state.message !== "" ?
		(<span className="message">{this.state.message}</span>) :
		(<span></span>);
		return(
			<div>
				<div id="video-wrapper" ref="videoWrapperRef" height="416" width="554">
					<video className={videoSourceClass} ref="videoRef" height="416" width="554"></video>
					<canvas className={canvasClass} ref="canvasOutRef" height="416" width="554"></canvas>
					<canvas className="block-hid" ref="canvasAuxRef" height="416" width="554"></canvas>
				</div>
				<div className={sourceButtonsClass}>
					<span className="button" id="camera-button" onClick={this.startCamera.bind(this)}></span>
					<span className="button" id="folder-button" onClick={this.bindToInput.bind(this)}></span>
					<input className="button" id="image-input" ref="inputImgRef" type="file" accept="image/*" onChange={this.loadImage.bind(this)}/>
				</div>
				<div className={shootButtonsClass}>
					<span className="button" id="shooter-button" onClick={this.shoot.bind(this)}></span>
				</div>
				<div className="message-container">
					{message}
				</div>
			</div>
		);
	}
}
//
let yoloDetector;
(async function main() {
  try {
	addLoadingVisual();

	let model = await downloadModel(assetUrl('model'));
	yoloDetector = new YoloDetector(model);

	doneLoading();
  } catch(e) {
	console.error(e);
	showError();
  }
})();

function doneLoading() {
	let FinderViewRendered = ReactDOM.render(<FinderView />, document.getElementById('boardDiv'));
	let loadingMessage = document.getElementById("loading-message");
	loadingMessage.className =  "block-hid";
}

function showError() {
  // TODO: Implement error message
}

function addLoadingVisual() {
	let container = document.getElementById("loading-message");

	let message = document.createElement('span');
	message.innerText = 'Loading module ...';

	let image = document.createElement('img');
	image.src = assetUrl('logo');
	image.className = "spin";

	let imageContainer = document.createElement('div');
	imageContainer.appendChild(image);

	container.appendChild(message);
	container.appendChild(imageContainer);
}

// This is a workaround to get the url of assets.
// The url are passed to the html template as flask parameters.
function assetUrl(domElemId) {
	let domElem = document.getElementById(domElemId);
	return domElem.getAttribute('url')
}