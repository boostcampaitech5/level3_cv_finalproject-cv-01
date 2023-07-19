package com.example.myapplication

import android.graphics.Color
import android.opengl.Visibility
import android.os.Bundle
import android.text.Spannable
import android.text.SpannableString
import android.text.SpannableStringBuilder
import android.text.style.ForegroundColorSpan
import android.util.Log
import com.google.android.material.bottomsheet.BottomSheetDialogFragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.LinearLayout
import androidx.fragment.app.Fragment
import com.example.myapplication.databinding.FragmentResultDialogBinding
import com.google.android.material.bottomsheet.BottomSheetBehavior
import com.google.android.material.bottomsheet.BottomSheetBehavior.BottomSheetCallback

class ResultListDialog : Fragment() {

    private lateinit var binding: FragmentResultDialogBinding
    // This property is only valid between onCreateView and
    // onDestroyView.
    private lateinit var behavior: BottomSheetBehavior<LinearLayout>
    private lateinit var main_data: resultData
    private lateinit var sub_data1: resultData
    private lateinit var sub_data2: resultData
    val class_dict = SHARED_DATA.data.class_dict
    val ingredients_dict = SHARED_DATA.data.ingredients_dict
    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {

        super.onCreateView(inflater, container, savedInstanceState)
        Log.d("test","bottom frag init")

        binding = FragmentResultDialogBinding.inflate(inflater, container, false)

        Log.d("test",container.toString())
        return binding.root
    }
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
//        Log.d("test",binding.infoLayout.toString())

        try {
            //버튼 설정
            binding.floatingActionButton.setImageResource(com.google.android.material.R.drawable.material_ic_menu_arrow_up_black_24dp)
            binding.floatingActionButton.setOnClickListener{
                toggle_bottomsheet()
            }
            //서브 text 클릭 설정
            binding.subInfo1.setOnClickListener{
                main_data = sub_data1.also{sub_data1 = main_data}
                setTextInfo(0)
                setTextInfo(1)
            }
            binding.subInfo2.setOnClickListener{
                main_data = sub_data2.also{sub_data2 = main_data}
                setTextInfo(0)
                setTextInfo(2)
            }

            behavior = BottomSheetBehavior.from(binding.infoVertical)
            behavior.addBottomSheetCallback(object: BottomSheetCallback(){
                override fun onStateChanged(bottomSheet: View, newState: Int) {
                    when(newState){
                        BottomSheetBehavior.STATE_COLLAPSED ->{
                            Log.d("test","close")
                            binding.floatingActionButton.setImageResource(com.google.android.material.R.drawable.material_ic_menu_arrow_up_black_24dp)
                        }
                        BottomSheetBehavior.STATE_EXPANDED ->{
                            Log.d("test","open")
                            binding.floatingActionButton.setImageResource(com.google.android.material.R.drawable.material_ic_menu_arrow_down_black_24dp)
                        }
                    }
                }

                override fun onSlide(bottomSheet: View, slideOffset: Float) {

                }
            })
            behavior.peekHeight = 90
            //test시 activate_bottomsheet()
            //실제 배포시 deactivate
            deactivate_bottomsheet()

        }
        catch (exc:Exception){

            Log.d("test",binding.infoStringConstraint.toString())
            Log.d("test",exc.toString())
        }
//        behavior.state = BottomSheetBehavior.STATE_HALF_EXPANDED

    }
    fun setInfoData(server_data: serverData){
        val data = server_data.resultData
        main_data = data[0]
        sub_data1 = data[1]
        sub_data2 = data[2]
        setTextInfo(0)
        setTextInfo(1)
        setTextInfo(2)
        activate_bottomsheet()
    }
    fun translateRecipe(recipes: List<String>): SpannableStringBuilder {
        var translatedString = ""
        val checklist = SHARED_DATA.data.checklist

        val intersect_ingredients = checklist.filterValues{ it }.keys.intersect(main_data.recipes.toSet())
        translatedString = recipes.map{ingredients_dict[it]}.joinToString(" ")
        val spanText = SpannableStringBuilder(translatedString)
        for(dup in intersect_ingredients){
            var dup_kr = ingredients_dict[dup]
            val word_start = translatedString.indexOf(ingredients_dict[dup]!!)
            spanText.setSpan(ForegroundColorSpan(Color.parseColor("#ff0000")),word_start,word_start+dup_kr!!.length,
            Spannable.SPAN_EXCLUSIVE_EXCLUSIVE)
        }
        return spanText
    }
    fun makeSpanString(main_data: resultData): SpannableStringBuilder {
        var result_string = "음식 이름\n" + class_dict[main_data.class_name] + "\n알레르기 유발 식자재\n"
        var recipe_string = translateRecipe(main_data.recipes)
        recipe_string.insert(0,result_string)
        return recipe_string
    }
    fun setTextInfo(target_idx: Int){
        when(target_idx){
            0 -> {
                binding.mainInfo.setText(makeSpanString(main_data))
            }
            1 -> {
                binding.subInfo1.setText(class_dict[sub_data1.class_name])
            }
            2 -> {
                binding.subInfo2.setText(class_dict[sub_data2.class_name])
            }
        }
    }
    //bottom sheet 닫힘/열림 전환 함수
    fun toggle_bottomsheet(){
        Log.d("test","toggle")
        when(behavior.state){
            BottomSheetBehavior.STATE_COLLAPSED -> open_bottomsheet()
            BottomSheetBehavior.STATE_EXPANDED -> close_bottomsheet()
        }
    }
    fun close_bottomsheet(){
        behavior.state = BottomSheetBehavior.STATE_COLLAPSED
    }
    fun open_bottomsheet(){
        behavior.state = BottomSheetBehavior.STATE_EXPANDED
    }
    //bottom sheet 활성화 - send 버튼이 눌렸을 때 데이터를 전송받으면 정보창 활성화하는 함수
    fun activate_bottomsheet(){
        binding.floatingActionButton.isEnabled = true
        behavior.state = BottomSheetBehavior.STATE_EXPANDED
        behavior.isDraggable = true
    }
    //bottom sheet 비활성화 - 현재는 초기설정에만 사용되나 추후 어플리케이션 동작 알고리즘에 따라 추가 사용가능
    fun deactivate_bottomsheet(){
        binding.floatingActionButton.isEnabled = false
        behavior.state = BottomSheetBehavior.STATE_COLLAPSED
        behavior.isDraggable = false
    }
    fun setResult(server_data: serverData){
        binding.floatingActionButton.isEnabled = true
        behavior.state = BottomSheetBehavior.STATE_EXPANDED
        behavior.isDraggable = true


    }

}