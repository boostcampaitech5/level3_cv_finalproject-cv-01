package com.example.myapplication

import android.graphics.Bitmap
import android.media.Image
import java.nio.ByteBuffer


data class JSONDATA(val class_dict: HashMap<String,String>, val ingredients_dict: HashMap<String,String>,
                    val checklist: MutableMap<String,Boolean>, val IP: String, val PORT: Int, val version:String)
object SHARED_DATA {
    var bitmap: Bitmap? = null
    var image_byte: ByteArray? = null
}
object USER_DATA {
    lateinit var data:JSONDATA
}