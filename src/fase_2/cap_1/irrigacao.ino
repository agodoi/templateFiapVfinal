#include <Arduino.h>
#include <DHT.h>
#include <math.h>

constexpr uint8_t PIN_NITROGENIO = 16;
constexpr uint8_t PIN_FOSFORO = 18;
constexpr uint8_t PIN_POTASSIO = 17;
constexpr uint8_t PIN_LDR = 34;
constexpr uint8_t PIN_DHT = 4;
constexpr uint8_t PIN_RELE = 23;

enum class Cultura : uint8_t
{
  SOJA,
  CAFE,
};

struct ParametrosIrrigacao
{
  float umidadeMinima;
  float umidadeMaxima;
  float phMinimo;
  float phMaximo;
};

constexpr ParametrosIrrigacao PARAMETROS_SOJA = {60.0f, 80.0f, 6.0f, 7.0f};
constexpr ParametrosIrrigacao PARAMETROS_CAFE = {70.0f, 80.0f, 5.5f, 6.5f};

// Defina a cultura ativa para alinhar a logica da Fase 2 com a cultura escolhida na Fase 1.
constexpr Cultura CULTURA_ATIVA = Cultura::SOJA;

const char *nomeCultura(Cultura cultura)
{
  return cultura == Cultura::SOJA ? "SOJA" : "CAFE";
}

ParametrosIrrigacao obterParametros(Cultura cultura)
{
  return cultura == Cultura::SOJA ? PARAMETROS_SOJA : PARAMETROS_CAFE;
}

DHT dht(PIN_DHT, DHT22);

float lerPH(int leituraAnalogica)
{
  return (leituraAnalogica / 4095.0f) * 14.0f;
}

void setup()
{
  Serial.begin(115200);
  analogReadResolution(12);

  pinMode(PIN_NITROGENIO, INPUT_PULLUP);
  pinMode(PIN_FOSFORO, INPUT_PULLUP);
  pinMode(PIN_POTASSIO, INPUT_PULLUP);
  pinMode(PIN_RELE, OUTPUT);

  digitalWrite(PIN_RELE, LOW);
  dht.begin();

  Serial.println("FarmTech Solutions - Irrigação Inteligente");
  Serial.print("Cultura ativa: ");
  Serial.println(nomeCultura(CULTURA_ATIVA));
}

void loop()
{
  const bool nitrogenio = digitalRead(PIN_NITROGENIO) == LOW;
  const bool fosforo = digitalRead(PIN_FOSFORO) == LOW;
  const bool potassio = digitalRead(PIN_POTASSIO) == LOW;

  const int leituraLdr = analogRead(PIN_LDR);
  const float ph = lerPH(leituraLdr);

  const float umidade = dht.readHumidity();
  const bool umidadeValida = !isnan(umidade);
  const ParametrosIrrigacao parametros = obterParametros(CULTURA_ATIVA);

  const bool irrigar = umidadeValida &&
                       umidade < parametros.umidadeMinima &&
                       nitrogenio &&
                       fosforo &&
                       potassio &&
                       ph >= parametros.phMinimo &&
                       ph <= parametros.phMaximo;

  digitalWrite(PIN_RELE, irrigar ? HIGH : LOW);

  Serial.print("N=");
  Serial.print(nitrogenio ? "1" : "0");
  Serial.print(" P=");
  Serial.print(fosforo ? "1" : "0");
  Serial.print(" K=");
  Serial.print(potassio ? "1" : "0");
  Serial.print(" | LDR=");
  Serial.print(leituraLdr);
  Serial.print(" | pH=");
  Serial.print(ph, 1);
  Serial.print(" [");
  Serial.print(parametros.phMinimo, 1);
  Serial.print("-");
  Serial.print(parametros.phMaximo, 1);
  Serial.print("]");
  Serial.print(" | umidade=");
  if (umidadeValida)
  {
    Serial.print(umidade, 1);
  }
  else
  {
    Serial.print("N/D");
  }
  Serial.print("% [");
  Serial.print(parametros.umidadeMinima, 1);
  Serial.print("-");
  Serial.print(parametros.umidadeMaxima, 1);
  Serial.print("%]");
  Serial.print(" | bomba=");
  Serial.println(irrigar ? "LIGADA" : "DESLIGADA");

  delay(2000);
}
