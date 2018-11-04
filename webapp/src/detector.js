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

module.exports = {
	Detector: Detector
};
