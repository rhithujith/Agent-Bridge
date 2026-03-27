import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  // We will get this URL from your teammate (Person 2) soon.
  // For now, we use a placeholder.
  static const String baseUrl = "https://agentbridge-demo.railway.app";
  static const String apiKey = "ab_demo_123";

  // This function fetches the logs from the server
  static Future<List<dynamic>> fetchLogs() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/logs?api_key=$apiKey'));

      if (response.statusCode == 200) {
        // If the server says "OK", return the list of logs
        return json.decode(response.body);
      } else {
        print("Server Error: ${response.statusCode}");
        return [];
      }
    } catch (e) {
      print("Connection Error: $e");
      return [];
    }
  }
}