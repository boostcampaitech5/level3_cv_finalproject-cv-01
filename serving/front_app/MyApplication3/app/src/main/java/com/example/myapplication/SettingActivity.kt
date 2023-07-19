package com.example.myapplication

import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.CheckBox
import android.widget.CompoundButton
import androidx.appcompat.app.AppCompatActivity
import com.example.myapplication.databinding.ActivitySettingBinding

import com.example.myapplication.SHARED_DATA
import com.google.gson.Gson
import java.io.File
import java.lang.Exception

class SettingActivity : AppCompatActivity() {

    private lateinit var binding: ActivitySettingBinding
    private val shared_data = SHARED_DATA
    private var checklist:MutableMap<String, Boolean> = shared_data.data.checklist
    private val ingredient_dict = shared_data.data.ingredients_dict
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = ActivitySettingBinding.inflate(layoutInflater)
        setContentView(binding.root)
        binding.settingRevertBnt.setOnClickListener{
            val gson = Gson()
            val jsonString = gson.toJson(shared_data.data)
            val file = File(filesDir,"user_data.json")
            file.writeText(jsonString)
            finish()
        }
        createChecklist(checklist)
    }
    //데이터 관리를 용이하게 하기 위해 런타임에 체크박스 생성하도록 구현
    fun createChecklist(checklist:MutableMap<String,Boolean>){
        val checkBoxListener = CompoundButton.OnCheckedChangeListener{
            buttonView, isChecked ->
//            Log.d("test",buttonView.text.toString()+isChecked.toString())

            val key:String = buttonView.tag.toString()
            checklist[key] = isChecked

        }

        for (check in checklist){
//            Log.d("test",check.key)
            val checkbox = CheckBox(this).apply{
                text = ingredient_dict[check.key]
                tag = check.key
                isChecked = check.value
            }
            checkbox.setOnCheckedChangeListener(checkBoxListener)
            binding.checklistLayout.addView(checkbox)
        }
    }
}
