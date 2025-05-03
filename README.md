# degroctf_2024-2025

### По сложности от сложного к легкому

### Все таски могут быть в разной мере охарактеризованы *уцуцугами*

## [****] D3GR 4LL-A: Uwutism Action (Rev 500) [ninefid] [x|x|_]

Кажется, у вас имеется проблема с варонавыком

### Решение:

Доступные тяги:

|Adelhyde RUSH|Plan B: Cfe|Monstew Deltergy|
|:-----------:|:---------:|:--------------:|
|Flanersh Nrg |*shaker*   |Kared Bulline   |

Секретный Рецепт:

4/0/1/0/5

Увидеть что отказ выглядит как `That's not what I wanted`

В гидре `search` `encoded string` и найдется одна `DAT_0057...`

Найти где она используется и это будет if стейтмент отказа

Чуть вышел будет `runtime_concatstr2("Perfect! " и странная чушь)`

Странная чушь указана чуть выше (просто сборка массива байтв):

```
    local_29f2 = 0x6564;
    local_29f0 = 0x775f6b795f6f7267;
    local_29e8 = 0x645f796568745f6f;
  /* /home/ninefid/proj/degroctf_2024-2025/d3gr.go:168 */
    local_29e0 = 0x737975675f325f6f;
  /* /home/ninefid/proj/degroctf_2024-2025/d3gr.go:169 */
    local_29d8 = 0x73755f656b696c5f;
  /* /home/ninefid/proj/degroctf_2024-2025/d3gr.go:170 */
    local_29d0 = 0x637333735f6e695f;
  /* /home/ninefid/proj/degroctf_2024-2025/d3gr.go:172 */
    runtime_concatstring2(0,"Perfect! ",9,&local_29f2,0x2a);
```

Клод Соннет смог преобразовать это во флаг:

`degro_yk_wo_they_do_2_guys_like_us_in_s3sc`

## [***.] loudy fish (PPC 400) [lukramancer] [x|_|_]

Here's a fish on the line and it is screaming for some times. Understand what it is saying.

`nc ip port`

### Решение:

Кричащая рыба:

```

+-----------------+        
|   morse_state   |        
+-----------------+        
                   \       
                    <0)))><
```

`morse_state` меняется между `SCREAMING` и `/SILENCE/`

Я без понятия как там у него сделано dot/dash, но работает

`DEGRO FISH SPEAK UPTO YOU , ` [повтор] -> `degro_fish_speak_upto_you`

Общая либа [mosre.py](loudyfish/morse.py)

Сервер [task.py](loudyfish/task.py)

Авторский солвер (на общей либе) [solve.py](loudyfish/solve.py)

## [**..] Gorbusha in rc Shell (CTB 300) [ninefid] [x|x|_]

Попадите в Section 9, выберитесь, и найдите флаг

```shell
nc ip port
```

// Контейнер у вас один на всех, просьба не ломать (я могу его спокойно перезапустить, но надеюсь вы придумаете взаимодействие повеселее окирпичивания)

### Решение:

Алпайн контейнер, подключение к сокату выдает `chroot` в /usr/lib/plan9 (пакет `plan9port`), но в котором есть `/dev` и `/proc` контейнера

Чрут запускает `/bin/rc -i`

В `/dev`, вероятно, ничего интересного нет (постарался как мог и вроде бы не допустил docker escape)

А вот в `/proc` находятся процессы алпайн-контейнера из которого был выполнен сокат чрут (PID 1)

```shell
cd /proc/1/root
```

И мы попадаем в / уже алпайна, где есть /flag.txt

`degro_th3y_st1ll_avoid_plan9`

[docker-compose.yml](GirS/docker-compose.yml)

[Dockerfile](GirS/Dockerfile)

[START.sh](GirS/START.sh)

## [**..] Потому что вы УВОЛЕНЫ (Web 200) [medovsq + alinarrg -> ninefid] [0|0|0]

Взять залупу с безумхака и доделать ее

На странице регистрации (или где-то) будет iframe вставка но url будет содержать креды пользователя (потому что вход через параметры) и в его чатах будет чат с флагом

## [*...] СЫР-8 был ошибкой (Stega 200) [ninefid] [x|x|_]

`🧀🍔󠅔󠅕󠅗󠅢󠅟󠅏󠅑󠅝󠅕󠅢󠅙󠅓󠅑󠅞󠅣󠅏󠅒󠅕󠅏󠅕󠅑󠅤󠅙󠅞󠅗󠅏󠅓󠅘󠅕󠅕󠅣󠅕󠅔󠅏󠅒󠅥󠅢󠅗󠅘󠅑󠅣`

### Решение:

https://emoji.paulbutler.org/?mode=decode

Перевод на [питончик](syr_sosal/syr_sosal.py)

`degro_americans_be_eating_cheesed_burghas`

## [**..] Негодяй (Foren 100) [ninefid] [0|0|0]

...

### Решение:

Файл [B58.png](bastard/B58.png) - PNG рисунок Bad Dragon дилдо. К сожалению, через `grep 'degro_'` таска не решается, но в конце файла есть:

```
[PNG DATA...]

--- CUT HERE ---

[ZIP DATA...]
```

Если оставить только `[ZIP DATA...]` (хотя и это можно не делать), то zip архив распакует файл flag.txt со строкой `UFRKfn7jjyBAeQyHejMqDbcmm1e8jZ`

Название файла `B58` отсылает к кодировке `base58`

`degro_b4se58_1s_bettah`

## Допом контест на фейковый статический сайт для прятанья влессов (??)

...

