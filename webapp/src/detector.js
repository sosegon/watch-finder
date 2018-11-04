import * as tf from '@tensorflow/tfjs';
import yolo from "./index_yolo";

class Detector {
	constructor(haar_file, utils) {
		this.haar_file = haar_file;
		this.classifier = new cv.CascadeClassifier();
		this.detections = new cv.RectVector();
		let self = this;

		utils.createFileFromUrl(this.haar_file, this.haar_file, () => {
			self.classifier.load(self.haar_file);
			console.log("Cascade file downloaded!");
		});
	}
	detect(srcMat){
		// Pre-processing
		let gray = new cv.Mat();
		cv.cvtColor(srcMat, gray, cv.COLOR_RGBA2GRAY, 0);
		// cv.equalizeHist(gray, gray);
		// let ksize = new cv.Size(3, 3);
		// let anchor = new cv.Point(-1, -1);
		// cv.blur(gray, gray, ksize, anchor, cv.BORDER_DEFAULT);

		this.classifier.detectMultiScale(gray, this.detections, 5.1, 6, 0);
		gray.delete();
	}
	drawDetections(srcMat, canvas, limit) {
		for(let i = 0; i < this.detections.size(); i++) {
			if(i >= limit) {
				break;
			}
			let object = this.detections.get(i);
			let point1 = new cv.Point(object.x, object.y);
			let point2 = new cv.Point(object.x + object.width, object.y + object.height);
			cv.rectangle(srcMat, point1, point2, [255, 0, 0, 255]);
		}
		cv.imshow(canvas, srcMat)
	}
	drawBoxes(srcMat, canvas, boxes) {
		boxes.forEach(box => {
			const {
				top, left, bottom, right, classProb, className,
			} = box;
			if(className === "clock") {
				// 69 corrects for the aspect ratio
				let point1 = new cv.Point(left + 69, top);
				let point2 = new cv.Point(right + 69, bottom);
				cv.rectangle(srcMat, point1, point2, [255, 0, 0, 255]);
			}
		});
		cv.imshow(canvas, srcMat);
	}
	extract(srcMat, detections) {
		let mats = [];
		for (let i = 0; i < this.detections.size(); ++i) {
			let object = this.detections.get(i);
			let dst = new cv.Mat();
			dst = srcMat.roi(object);
			mats.push(dst);
		}
		return mats;
	}
}

class YoloDetector {
	constructor(model) {
		this.model = model;
	}
	cropImage(img) {
		const size = Math.min(img.shape[0], img.shape[1]);
		const centerHeight = img.shape[0] / 2;
		const beginHeight = centerHeight - (size / 2);
		const centerWidth = img.shape[1] / 2;
		const beginWidth = centerWidth - (size / 2);
		return img.slice([beginHeight, beginWidth, 0], [size, size, 3]);
	}
	captureVideo(videoElem) {
		let self = this;

		return tf.tidy(() => {
			// Reads the image as a Tensor from the webcam <video> element.
			const webcamImage = tf.fromPixels(videoElem);

			// Crop the image so we're using the center square of the rectangular
			// webcam.
			const croppedImage = self.cropImage(webcamImage);

			// Expand the outer most dimension so we have a batch size of 1.
			const batchedImage = croppedImage.expandDims(0);

			// Normalize the image between -1 and 1. The image comes in between 0-255,
			// so we divide by 127 and subtract 1
			return batchedImage.toFloat().div(tf.scalar(255));
		});
	}
	async detectObjects(videoElem) {
		const inputImage = this.captureVideo(videoElem);

		const t0 = performance.now();
		const boxes = await yolo(inputImage, this.model);
		inputImage.dispose();
		const t1 = performance.now();

		console.log("YOLO inference took " + (t1 - t0) + " milliseconds.");
		console.log('tf.memory(): ', tf.memory());

		await tf.nextFrame();

		return boxes;
	}
}

module.exports = {
	Detector: Detector,
	YoloDetector: YoloDetector
};
