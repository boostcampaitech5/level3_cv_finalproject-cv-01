package com.example.myapplication

import android.graphics.Bitmap
import androidx.camera.core.ImageProxy


data class JSONDATA(val class_dict: HashMap<String,String>, val ingredients_dict: HashMap<String,String>,
                    val checklist: MutableMap<String,Boolean>, val IP: String, val PORT: Int)
object SHARED_DATA {
    var bitmap: Bitmap? = null
    var image: ImageProxy? = null

    lateinit var data: JSONDATA
}
