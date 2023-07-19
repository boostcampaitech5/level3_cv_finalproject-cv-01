package com.example.myapplication

import android.graphics.Bitmap
import com.google.gson.annotations.SerializedName
import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST
import java.nio.ByteBuffer


data class clientData(
    val image: ByteArray,
)
data class serverData(
    @SerializedName("result")
    var resultData: List<resultData>
)
data class resultData(
    @SerializedName("class")
    val class_name: String,
    @SerializedName("recipe")
    val recipes: List<String>,
    @SerializedName("valid")
    val valid: Boolean
)
interface RetrofitService {
    @POST("/upload")
    fun getResult(@Body data: clientData) : Call<serverData>
    @GET("/test")
    fun test() : Call<String>

}