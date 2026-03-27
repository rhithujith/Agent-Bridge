import 'package:flutter/material.dart';
import 'dart:async';
import 'api_service.dart';

void main() {
  runApp(const AgentBridgeApp());
}

class ABColors {
  static const bg = Color(0xFF0B0E14);
  static const surface = Color(0xFF13151A);
  static const card = Color(0xFF1A1D24);
  static const accent = Color(0xFF00E5B0);
  static const danger = Color(0xFFE05555);
  static const warn = Color(0xFFF0A500);
  static const text = Color(0xFFF0F1F4);
  static const muted = Color(0xFF9097AA);
}

class AgentBridgeApp extends StatelessWidget {
  const AgentBridgeApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'AgentBridge Dashboard',
      theme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: ABColors.bg,
        cardColor: ABColors.card,
      ),
      home: const MainDashboard(),
    );
  }
}

class MainDashboard extends StatefulWidget {
  const MainDashboard({super.key});

  @override
  State<MainDashboard> createState() => _MainDashboardState();
}

class _MainDashboardState extends State<MainDashboard> {
  int _selectedIndex = 0;
  List<dynamic> logs = [];
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    _loadData();
    // Refresh every 5 seconds
    _timer = Timer.periodic(const Duration(seconds: 5), (timer) {
      _loadData();
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  void _loadData() async {
    final incomingLogs = await ApiService.fetchLogs();
    if (mounted) {
      setState(() {
        logs = incomingLogs;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Row(
        children: [
          NavigationRail(
            backgroundColor: ABColors.surface,
            selectedIndex: _selectedIndex,
            onDestinationSelected: (i) => setState(() => _selectedIndex = i),
            labelType: NavigationRailLabelType.all,
            unselectedIconTheme: const IconThemeData(color: ABColors.muted),
            selectedIconTheme: const IconThemeData(color: ABColors.accent),
            destinations: const [
              NavigationRailDestination(icon: Icon(Icons.grid_view_rounded), label: Text('Dashboard')),
              NavigationRailDestination(icon: Icon(Icons.warning_amber_rounded), label: Text('Incidents')),
              NavigationRailDestination(icon: Icon(Icons.description_outlined), label: Text('Report')),
            ],
          ),
          Expanded(
            child: Padding(
              padding: const EdgeInsets.all(32.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _buildHeader(),
                  const SizedBox(height: 32),
                  _buildSummaryCards(),
                  const SizedBox(height: 32),
                  const Text("LIVE ACTION FEED", style: TextStyle(color: ABColors.muted, fontWeight: FontWeight.bold, letterSpacing: 1.2)),
                  const SizedBox(height: 16),
                  Expanded(child: _buildLogTable()),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildHeader() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        const Text("AgentBridge / Monitoring", style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: ABColors.text)),
        Row(
          children: [
            const Icon(Icons.circle, color: ABColors.accent, size: 10),
            const SizedBox(width: 8),
            Text("System Live: ${logs.length} Actions", style: const TextStyle(color: ABColors.muted)),
          ],
        )
      ],
    );
  }

  Widget _buildSummaryCards() {
    return Row(
      children: [
        _metricCard("Active Agents", "3", Icons.bolt, ABColors.accent),
        _metricCard("Total Actions", logs.length.toString(), Icons.list, ABColors.text),
        _metricCard("Open Incidents", logs.where((l) => l['flagged'] == true).length.toString(), Icons.error_outline, ABColors.danger),
        _metricCard("Compliance Score", "94%", Icons.verified_user, ABColors.accent),
      ],
    );
  }

  Widget _metricCard(String title, String value, IconData icon, Color color) {
    return Expanded(
      child: Container(
        margin: const EdgeInsets.only(right: 16),
        padding: const EdgeInsets.all(24),
        decoration: BoxDecoration(color: ABColors.surface, borderRadius: BorderRadius.circular(12)),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Icon(icon, color: color, size: 20),
            const SizedBox(height: 16),
            Text(value, style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold)),
            Text(title, style: const TextStyle(color: ABColors.muted, fontSize: 14)),
          ],
        ),
      ),
    );
  }

  Widget _buildLogTable() {
    // If on Incidents tab, only show flagged ones
    final displayLogs = _selectedIndex == 1
        ? logs.where((l) => l['flagged'] == true).toList()
        : logs;

    return Container(
      decoration: BoxDecoration(
        color: ABColors.surface,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.white.withOpacity(0.05)),
      ),
      child: ListView.separated(
        itemCount: displayLogs.length,
        separatorBuilder: (context, index) => Divider(color: Colors.white.withOpacity(0.05), height: 1),
        itemBuilder: (context, index) {
          final log = displayLogs[index];
          final bool isFlagged = log['flagged'] ?? false;
          return ListTile(
            contentPadding: const EdgeInsets.symmetric(horizontal: 24, vertical: 8),
            leading: Text(
                log['created_at'] != null ? log['created_at'].toString().substring(11, 16) : "--:--",
                style: const TextStyle(color: ABColors.muted, fontFamily: 'monospace')
            ),
            title: Text(log['action'] ?? "Action", style: TextStyle(color: isFlagged ? ABColors.danger : ABColors.text, fontWeight: FontWeight.w600)),
            subtitle: Text("Input: ${log['inputs'] ?? 'None'}", style: const TextStyle(color: ABColors.muted), maxLines: 1),
            trailing: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(isFlagged ? "FLAGGED" : (log['status'] ?? "success"), style: TextStyle(color: isFlagged ? ABColors.danger : ABColors.accent, fontWeight: FontWeight.bold)),
                const SizedBox(width: 20),
                Text("${log['latency_ms'] ?? 0}ms", style: const TextStyle(color: ABColors.muted)),
              ],
            ),
          );
        },
      ),
    );
  }
}