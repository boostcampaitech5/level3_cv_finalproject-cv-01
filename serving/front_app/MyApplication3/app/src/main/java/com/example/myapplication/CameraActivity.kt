package com.example.myapplication

import android.app.Activity
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.ImageFormat
import android.graphics.Matrix
import android.graphics.Rect
import android.graphics.YuvImage
import android.media.Image
import android.os.Bundle
import android.util.Log
import android.view.Surface.ROTATION_0
import android.view.Surface.ROTATION_180
import android.view.Surface.ROTATION_270
import android.view.Surface.ROTATION_90
import androidx.appcompat.app.AppCompatActivity
import androidx.camera.core.CameraSelector
import androidx.camera.core.ImageCapture
import androidx.camera.core.ImageCaptureException
import androidx.camera.core.ImageProxy
import androidx.camera.core.Preview
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.camera.view.PreviewView
import androidx.core.content.ContextCompat
import com.example.myapplication.databinding.ActivityCameraBinding
import java.io.ByteArrayOutputStream
import java.lang.Integer.max
import java.lang.Integer.min


class CameraActivity : AppCompatActivity() {
    private lateinit var binding: ActivityCameraBinding
    private lateinit var imageCapture: ImageCapture
    private val sharedData = SHARED_DATA
    private lateinit var previewView: PreviewView
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding =ActivityCameraBinding.inflate(layoutInflater)
        setContentView(binding.root)
        previewView = binding.viewFinder
        binding.revert.setOnClickListener {
            finish()
        }
        binding.capture.setOnClickListener {
            captureCamera { image ->
                //임시로 bitmap대신 proxy 반환.
//                sharedData.bitmap = bitmap
//                sharedData.image = image
//                var bitmap = imageProxyToBitmap(image)

                sharedData.bitmap = imageProxyToBitmap(image)



                Log.d("test", sharedData.bitmap.toString())

                val result = Intent().apply {
                    putExtra("from_activity", "camera")
                    if (image == null) {
                        Log.d("test", "Camera not available")
                        putExtra("success", false)
                    } else {
                        putExtra("success", true)
                    }
                }

                setResult(Activity.RESULT_OK, result)
                finish()
            }
        }
        startCamera()
    }


    fun captureCamera(callback: (ImageProxy?) -> Unit) {
        imageCapture.takePicture(ContextCompat.getMainExecutor(this),
            object : ImageCapture.OnImageCapturedCallback() {
                override fun onCaptureSuccess(image: ImageProxy) {
                    //현재 bitmap 변환이 문제가 있어서 imgproxy 반환중
//                    val bitmap = imageProxyToBitmap(image)

                    Log.d("test","camear capture success")
//                    callback(bitmap)
                    callback(image)
                }

                override fun onError(exception: ImageCaptureException) {
                    Log.d("test", "image capture error: ${exception.message}")
                    callback(null)
                }
            }
        )
    }

    private fun startCamera() {
        binding.viewFinder.scaleType = PreviewView.ScaleType.FIT_CENTER
        val cameraProviderFuture = ProcessCameraProvider.getInstance(this)
        cameraProviderFuture.addListener({
            val cameraProvider = cameraProviderFuture.get()
            val preview = Preview.Builder().build().also {
                it.setSurfaceProvider(binding.viewFinder.surfaceProvider)
            }
            imageCapture = ImageCapture.Builder().build()

            val cameraSelector = CameraSelector.DEFAULT_BACK_CAMERA

            try {
                cameraProvider.unbindAll()
                cameraProvider.bindToLifecycle(this, cameraSelector, preview, imageCapture)
            } catch (exc: Exception) {
                Log.e("CameraX", "Use case binding failed", exc)
            }
        }, ContextCompat.getMainExecutor(this))

    }
    private fun updateTransform() {
        val matrix = Matrix()

        // 디스플레이 회전에 따라 보정
        val rotationDegrees = when (previewView.display.rotation) {
            ROTATION_0 -> 0
            ROTATION_90 -> 90
            ROTATION_180 -> 180
            ROTATION_270 -> 270
            else -> 0
        }
//        Log.d("test",rotationDegrees.toString())
        // 카메라 센서와 디스플레이의 회전 각도 보정
        matrix.postRotate(-rotationDegrees.toFloat(), previewView.width / 2f, previewView.height / 2f)

    }
    private fun imageProxyToBitmap(imageProxy: ImageProxy?): Bitmap? {

        try {
            if (imageProxy != null) {
                @androidx.camera.core.ExperimentalGetImage
                val image: Image? = imageProxy.image

                val buffer = image!!.planes[0].buffer
                val bytes = ByteArray(buffer.capacity()).also { buffer.get(it) }
//                sharedData.image_byte = bytes.clone()
                var bitmap:Bitmap = BitmapFactory.decodeByteArray(bytes, 0, bytes.size)
                var height= bitmap.height
                var width = bitmap.width
                if(min(height,width)>256){
                    val pivot = min(height,width)/256.0
                    height = height.div(pivot).toInt()
                    width = width.div(pivot).toInt()
                }
                bitmap = Bitmap.createScaledBitmap(bitmap,width,height,true)

                Log.d("test","rotate:${imageProxy.imageInfo.rotationDegrees}")
                val rotationDegrees = when (imageProxy.imageInfo.rotationDegrees) {
                    0 -> 0
                    90 -> 90
                    180 -> 180
                    270 -> 270
                    else -> 0
                }
                val matrix = Matrix()
                matrix.postRotate(rotationDegrees.toFloat())
                bitmap = Bitmap.createBitmap(bitmap, 0, 0, width, height, matrix, true)
                val out_stream = ByteArrayOutputStream()
                bitmap.compress(Bitmap.CompressFormat.JPEG,100,out_stream)
                sharedData.image_byte = out_stream.toByteArray()
                return bitmap
            }
            return null
        }
        catch (exc:Exception){
            Log.d("test","convert : "+exc.toString())
            return null
        }
    }

}