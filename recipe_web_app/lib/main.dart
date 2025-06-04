import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() => runApp(const RecipeApp());

class RecipeApp extends StatelessWidget {
  const RecipeApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '레시피 추천기',
      theme: ThemeData(primarySwatch: Colors.green),
      home: const RecipeHomePage(),
    );
  }
}

class RecipeHomePage extends StatefulWidget {
  const RecipeHomePage({super.key});

  @override
  State<RecipeHomePage> createState() => _RecipeHomePageState();
}

class _RecipeHomePageState extends State<RecipeHomePage> {
  final TextEditingController _controller = TextEditingController();
  List<dynamic> _recommendations = [];

  Future<void> fetchRecommendations() async {
    final ingredients = _controller.text.split(',').map((e) => e.trim()).toList();

    try {
      final response = await http.post(
        Uri.parse('http://127.0.0.1:8000/recommend'), // 서버 주소 확인
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({"ingredients": ingredients}),
      );

      if (response.statusCode == 200) {
        final decoded = jsonDecode(utf8.decode(response.bodyBytes)); // 💡 한글 깨짐 방지
        final List<dynamic> recs = decoded['recommendations'] ?? [];

        setState(() {
          _recommendations = recs;
        });
      } else {
        print("서버 응답 실패: ${response.statusCode}");
        print("본문: ${response.body}");
      }
    } catch (e) {
      print("요청 중 오류 발생: $e");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('레시피 추천기')),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            TextField(
              controller: _controller,
              decoration: const InputDecoration(
                labelText: '재료 입력 (예: 김치, 돼지고기)',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: fetchRecommendations,
              child: const Text('추천받기'),
            ),
            const SizedBox(height: 20),
            Expanded(
              child: ListView.builder(
                itemCount: _recommendations.length,
                itemBuilder: (context, index) {
                  final r = _recommendations[index];
                  final name = r['메뉴'] ?? '메뉴 없음';
                  final matchRate = (r['매칭률'] ?? 0.0) * 100;
                  final missingIngredients = r['부족재료'] ?? [];
                  final recipeText = r['레시피'] ?? '';
                  final products = r['추천상품'] ?? [];

                  return Card(
                    margin: const EdgeInsets.symmetric(vertical: 6),
                    child: Padding(
                      padding: const EdgeInsets.all(12.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text("$name (${matchRate.toInt()}%)", style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                          const SizedBox(height: 8),
                          Text("부족재료: ${missingIngredients.join(', ')}"),
                          const SizedBox(height: 8),
                          Text("레시피:\n$recipeText"),
                          const SizedBox(height: 8),
                          if (products.isNotEmpty)
                            Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                const Text("추천상품:", style: TextStyle(fontWeight: FontWeight.bold)),
                                ...products.map<Widget>((item) {
                                  final productName = item['이름'] ?? '이름 없음';
                                  final productPrice = item['가격'] ?? '?';
                                  final productUnit = item['단위'] ?? '?';
                                  return Text("- $productName ($productPrice/$productUnit)");
                                }).toList(),
                              ],
                            )
                        ],
                      ),
                    ),
                  );
                },
              ),
            )
          ],
        ),
      ),
    );
  }
}
