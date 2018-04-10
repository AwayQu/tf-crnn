//
//  main.swift
//  vision_text_detection
//
//  Created by MacDev on 2018/4/9.
//  Copyright © 2018年 MacDevHuang. All rights reserved.
//

import Foundation
import Cocoa

let ignore_file = ".DS_Store"

let basePath = "/Users/macdev/Documents/quyiming/ml/tf-crnn/data_extract"
//let basePath = "."

let dataPath = "\(basePath)/data"
let outputPath = "\(basePath)/output"



let fm = FileManager.default

print("Current directory path \(fm.currentDirectoryPath)")

guard fm.fileExists(atPath: dataPath) else {
    print("\(dataPath) path is not exists !")
    exit(1)
}


let enumerator = fm.enumerator(atPath: dataPath)
    
for f in enumerator! {
    guard let f = f as? String else {
        print("fd is not string !")
        exit(1)
    }
    if (f == ignore_file) {
        continue
    }

    let path = "\(dataPath)/\(f)"
    
    
//    let cfUrl = NSURL(fileURLWithPath: path) as CFURL
//    CGDataProvider(url: cfUrl)
    let semaphore = DispatchSemaphore(value: 1)
    guard let img = NSImage(contentsOf: URL(fileURLWithPath: path)) else {
        print("\(path) is not a img !")
        exit(2)
    }
    let detection = TextDetection()
    detection.semaphore = semaphore
    detection.inputImage = CIImage(cgImage: img.cgImage(forProposedRect: nil, context: nil, hints: nil)!)
    detection.textDetect(ciImage: detection.inputImage!)
    
    semaphore.wait()
    print(detection.resultImgs)
    
    for (index, ci) in detection.resultImgs.enumerated() {
        let rep = NSBitmapImageRep(ciImage: ci)
        let nsImg = NSImage(size: rep.size)
        nsImg.addRepresentation(rep)
        
        let imgData = rep.representation(using: .png, properties: [:])
        
        do {
            let fName = f.split(separator: ".").first!
            try imgData?.write(to: URL(fileURLWithPath: "\(outputPath)/\(fName)_\(index).png"))
        } catch {
            print("Write image error !")
        }
    }
    semaphore.signal()
    
}




